# import multiprocessing as mp
# import socket
# import signal
# from Watchdog import Watchdog
# import time
# import os

# socket_address = "test.sock"
# os.remove(socket_address)

# def server():
#     sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     sock.bind(socket_address)
#     sock.listen(1)
    
#     # for _ in range(4):
#     time.sleep(1)
#     client_conn, client_address = sock.accept()
#     client_conn.sendall(b"server sent")
#     recieve = sock.recv(11).decode("utf-8")
#     print(f"server got '{recieve}''")

# def client(cid):
#     sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     sock.connect(socket_address)
#     time.sleep(.5)
#     recieve = sock.recv(11).decode("utf-8")
#     sock.sendall(b"client sent")
#     print(f"client {cid} got '{recieve}''")

# s = mp.Process(target=server)
# c = mp.Process(target=client, args=(1, ))
# # s = [mp.Process(target=client, args=(cid,)) for cid in range(3)]

# s.start()
# time.sleep(.5)
# c.start()
# # for sp in s:
#     # sp.start()

# def foo():
#     for i in range(20):
#         print(i)
#         time.sleep(1)

# p = mp.Process(target=foo)
# p.start()

# def exit():
#     s.terminate()
#     c.terminate()
#     p.terminate()
#     print("exiting")

# Watchdog(2, exit).start()


from contextlib import ContextDecorator

class makeparagraph(ContextDecorator):
    def __enter__(self):
        print('<p>')
        return self

    def __exit__(self, *exc):
        print('</p>')
        return False

@makeparagraph()
def emit_html():
    print('Here is some non-HTML')

emit_html()


# with makeparagraph() as foo:
#     print('Here is some non-HTML')


with makeparagraph() as html:
    print("asdfasdf asdfsadf")



