#! /usr/bin/python3

import socket
import sys
import os
import subprocess

from config import socket_address, MAX_WORD_LEN, MAX_DEF_LEN

def wake_up_server():
    """
        wakes up server and waits until server is initialized
    """
    pipein, pipeout = os.pipe()

    # starting server
    FNULL = open(os.devnull, 'w')
    cmd = [sys.executable, "httppool_server.py"]
    server = subprocess.Popen(cmd, stdout=pipeout, 
        close_fds=False, bufsize=5) # closing stdout as alfred detects running workflows by open stdout.

    # client waiting for server to become ready
    recieved = os.read(pipein, 6)

def connect_to_server(socket_address: str) -> socket.socket:
    # Create socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # trying to connect to server
        sock.connect(socket_address)
        # found previous server
        
    except socket.error as msg:
        # server connection failed. starting server
        wake_up_server()
        sock.connect(socket_address)

    return sock

def query_datamuse(query: str) -> str:
    # querying manager for a worker process socket address
    sock = connect_to_server(socket_address)
    worker_address = sock.recv(MAX_WORD_LEN).strip(b"\0").decode("utf-8")
    
    # querying worker process for word suggestions and definition
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(worker_address)
    sock.sendall(query.encode()[:MAX_WORD_LEN].ljust(MAX_WORD_LEN, b"\0"))
    response = sock.recv(MAX_DEF_LEN).strip(b"\0").decode("latin-1")
    
    return response

if __name__ == "__main__":
    query_datamuse("sl=weat&max=10&md=d")
