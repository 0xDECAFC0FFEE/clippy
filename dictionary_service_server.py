#! /usr/bin/python

import socket
import os
from Watchdog import Watchdog 
from DictionaryServices import DCSCopyTextDefinition
import sys

sys.stdout.close()
sys.stdin.close()

server_address = './Alfred_Dictionary_Socket'
wd = Watchdog(10)
wd.start()

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except:
    pass

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# server alerting client that it is ready for input
# note that stderr has been redirected to client pipe
sys.stderr.write("ready")

while True:
    # Wait for a connection
    try:
        # pidprint('server waiting for client')
        connection, client_address = sock.accept()
        # pidprint('server found client')

        # accept each word and return its size
        while True:
            # refresh inactivity watchdog
            wd.refresh()

            word_to_define = connection.recv(200).strip()
            # pidprint('server recieved word %s' % word_to_define)
            if not word_to_define:
                break
            
            dictresult = DCSCopyTextDefinition(None, word_to_define, (0, len(word_to_define)))

            definition = dictresult if dictresult else ("%s not in osx dictionary" % word_to_define)

            definition = definition.encode('utf-8')[:200].ljust(200, " ")

            connection.sendall(definition)
    except Exception as e:
        print(e)

    finally:
        connection.close()
        # pidprint("closed connection")

