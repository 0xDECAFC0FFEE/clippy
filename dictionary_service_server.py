#! /usr/bin/python

import socket
import os
from Watchdog import Watchdog 
from DictionaryServices import DCSCopyTextDefinition
from config import MAX_DEF_LEN, SERVER_TIMEOUT_SECONDS
import sys

server_address = './Alfred_Dictionary_Socket'
wd = Watchdog(SERVER_TIMEOUT_SECONDS)
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
sys.stderr.write("ready\n")

while True:
    try:
        # server waiting for client
        connection, client_address = sock.accept()
        while True:
            # refresh inactivity watchdog
            wd.refresh()

            # recieve word. if an empty string is sent, means that the client is closing the connection
            word_to_define = str(connection.recv(MAX_DEF_LEN)).strip()
            sys.stderr.write("recieved word %s\n" % word_to_define)

            if not word_to_define:
                break
            
            # getting definition of word from dictionary app

            word_to_define = word_to_define.encode("utf-8")
            word_length = (0, len(word_to_define))

            # retrieving word from osx dictionary
            dictresult = DCSCopyTextDefinition(
                None, word_to_define, word_length)

            definition = dictresult.encode('utf-8') if dictresult else "%s not in osx dictionary" % word_to_define

            # padding definition to MAX_DEF_LEN characters cause alfred can't display more than that anyway probably
            definition = definition[:MAX_DEF_LEN].ljust(MAX_DEF_LEN, " ")

            # sending definition to client
            sys.stderr.write("sending definition %s.\n" % definition)
            connection.sendall(definition)
    except Exception as e:
        print(e)

    finally:
        connection.close()
