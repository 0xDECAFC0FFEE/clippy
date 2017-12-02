#! /usr/bin/python

import socket
import os
from Watchdog import Watchdog 
from DictionaryServices import DCSCopyTextDefinition
import sys

server_address = './Alfred_Dictionary_Socket'
wd = Watchdog(10)
wd.start()

# unlink previous server if it already exists for some reason
try:
    os.unlink(server_address)
except:
    pass

# Create a socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# server alerting client that it is ready for input
# note that stderr has been redirected to client pipe
sys.stderr.write("ready")

while True:
    try:
        # server waiting for client
        connection, client_address = sock.accept()
        while True:
            # refresh inactivity watchdog
            wd.refresh()

            # recieve word. if an empty string is sent, means that the client is closing the connection
            word_to_define = connection.recv(200).strip()
            if not word_to_define:
                break
            
            # getting definition of word from dictionary app
            dictresult = DCSCopyTextDefinition(None, word_to_define, (0, len(word_to_define)))
            definition = dictresult if dictresult else ("%s not in osx dictionary" % word_to_define)

            # padding definition to 200 characters
            definition = definition.encode('utf-8')[:200].ljust(200, " ")

            # sending definition to client
            connection.sendall(definition)
    except Exception as e:
        print(e)

    finally:
        connection.close()
