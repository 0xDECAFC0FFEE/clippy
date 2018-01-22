#! /usr/bin/python

import time
import socket
from sys import argv
import os
import subprocess
import random
from config import MAX_DEF_LEN

server_address = './Alfred_Dictionary_Socket'

def start_server():
    # creating pipe so server could alert client when ready
    pipein, pipeout = os.pipe()

    # starting server
    FNULL = open(os.devnull, 'w')
    cmd = ['/usr/bin/python', "dictionary_service_server.py"]
    server = subprocess.Popen(cmd, stdout=FNULL, stderr=pipeout, 
        close_fds=False, bufsize=5) # closing stdout as alfred detects running workflows by open stdout.
    
    # client waiting for server to become ready
    input = os.read(pipein, 6) # detecting server input from stderr as stdout is closed

def get_definitions(words):

    # Create socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # trying to connect to server
        sock.connect(server_address)
    except socket.error as msg:
        # server connection failed. starting server
        start_server()
        sock.connect(server_address)

    # communicating with server to get definitions
    # wrapping everything in a try except just to make sure socket is closed at the end
    words_dictionary = []
    try:
        for word in words:
            # sending server words and recieving definition
            sock.sendall(word[:MAX_DEF_LEN].ljust(MAX_DEF_LEN, " ").encode())
            definition = sock.recv(MAX_DEF_LEN).strip().decode("utf-8", "ignore") # ignoring decode errors cause the last couple code points could have been truncated
            words_dictionary.append((word, definition))

    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    return words_dictionary


if __name__ == "__main__":
    if len(argv) == 1:
        words = [b'frank', b'cool', b'cruel', b'poo', b'dana', b'red', b'reddit']
    else:
        words = argv[1:]
        words = [word.decode("utf-8") for word in words]
    print(get_definitions(words))
