#! /usr/bin/python
import os
import sys
import time

def pidprint(message):
    sys.stderr.write("server %s: %s\n" % (os.getpid(), message))

pipeout = int(sys.argv[1])

pidprint("writing to pipe %s" % pipeout)
os.write(pipeout, "ready")
