#! /usr/bin/python

import time
import socket
import sys
import os
import subprocess
import random

server_address = './Alfred_Dictionary_Socket'

def start_server():
    # creating pipe so server could alert client when ready
    pipein, pipeout = os.pipe()

    # starting server
    FNULL = open(os.devnull, 'w')
    cmd = ['/usr/bin/python', "dictionary_service_server.py"]
    server = subprocess.Popen(
        cmd, stdout=FNULL, stderr=pipeout, close_fds=False, bufsize=5)
    
    # client waiting for server to become ready
    input = os.read(pipein, 5)

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
            sock.sendall(word[:200].ljust(200, " "))
            definition = sock.recv(200)
            words_dictionary.append((word, definition))

        # closing connection to server
        sock.sendall(" "*200)

    finally:
        sock.close()

    return words_dictionary


if __name__ == "__main__":
    words = [b'frank', b'cool', b'cruel', b'poo', b'dana', b'red', b'reddit']
    print(get_definitions(words))
