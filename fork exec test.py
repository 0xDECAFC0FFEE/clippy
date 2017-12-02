import os
import sys
import time

def pidprint(message):
    sys.stderr.write("server %s: %s\n" % (os.getpid(), message))

pipein, pipeout = os.pipe()

pid = os.fork()
pidprint("forked process")

pidprint("pipein %s" % pipein)
pidprint("pipeout %s" % pipeout)

if pid == 0:
    location = "exec_test.py"
    pidprint("execing child")
    os.execv(location, [location, str(pipeout)])
else:
    time.sleep(1)
    pidprint("reading from pipe %s" % pipein)
    pidprint("child said %s" % os.read(pipein, 5))
