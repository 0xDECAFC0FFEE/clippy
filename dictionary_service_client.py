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
    server = subprocess.Popen(cmd, stdout=FNULL, stderr=pipeout, close_fds=False)
    
    # waiting for server to become ready
    input = os.read(pipein, 5)
    

def get_definitions(words):
    # Create socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # pidprint("connection opened")

    try:
        # trying to connect to server
        sock.connect(server_address)
    except socket.error as msg:
        # server connection failed. starting server
        start_server()
        sock.connect(server_address)

    # wrapping everything in a try except just to make sure socket is closed
    pidprint("communicating with server to get definitions")
    words_dictionary = []
    try:
        for word in words:
            # pidprint("client sending server %s" % word)
            sock.sendall(word[:200].ljust(200, " "))
            definition = sock.recv(200)
            words_dictionary.append((word, definition))

        sock.sendall(" "*200)

    except:
        pass
    finally:
        sock.close()
        pidprint("connection closed")

    pidprint("definitions recieved")

    return words_dictionary


if __name__ == "__main__":
    words = [b'frank', b'cool', b'cruel', b'poo', b'dana', b'red', b'reddit']
    print(get_definitions(words))
