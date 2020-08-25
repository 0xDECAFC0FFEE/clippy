#! /usr/bin/python3

import socket
from sys import argv, stderr
import os
import subprocess
from datamuse_httppool_server import server_address, MAX_WORD_LEN, MAX_DEF_LEN

def wake_up_server():
    # creating pipe so server could alert client when ready
    pipein, pipeout = os.pipe()

    # starting server
    FNULL = open(os.devnull, 'w')
    cmd = ['/usr/bin/python3', "datamuse_httppool_server.py"]
    server = subprocess.Popen(cmd, stdout=pipeout, 
        close_fds=False, bufsize=5) # closing stdout as alfred detects running workflows by open stdout.

    # client waiting for server to become ready
    os.read(pipein, 6) # detecting server input from stderr as stdout is closed

def connect_to_server(server_address):
    # Create socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        # trying to connect to server
        sock.connect(server_address)
    except socket.error as msg:
        # server connection failed. starting server
        wake_up_server()
        sock.connect(server_address)

    return sock

def query_datamuse(query):
    sock = connect_to_server(server_address)

    try:
        # sending server query and recieving definition
        sock.sendall(query.encode()[:MAX_WORD_LEN].ljust(MAX_WORD_LEN, b"\0"))
        response = sock.recv(MAX_DEF_LEN).strip(b"\0").decode("latin-1") # ignoring decode errors cause the last couple code points could have been truncated
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    return response