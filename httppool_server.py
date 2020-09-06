"""
manager daemon that manages worker threads. keeps the available ones in a queue

clients wake up server if not up, connect to manager socket and request a worker
manager daemon responds with worker socket address. if none are available, starts new worker
client then connects to worker and requests word suggestions
worker responds with suggestion
"""

import sys
import multiprocessing as mp
import os
from config import SERVER_TIMEOUT_SECONDS, socket_address, MAX_WORD_LEN, MAX_DEF_LEN
import socket
from Watchdog import Watchdog
import signal
from httppool_worker import Worker, workerid_to_socket

class Daemon():
    def start_new_worker(self) -> mp.Process:
        new_worker_id = len(self.worker_pool)
        new_worker_address = workerid_to_socket(new_worker_id)

        p = Worker(new_worker_id, self.available_workers)
        self.worker_pool.append(p)
        p.start()

        return p

    def __init__(self):
        sys.stderr.write("server starting up\n")
        sys.stderr.flush()
        self.worker_pool = []
        self.available_workers = mp.Queue()

        try:
            os.remove(socket_address)
        except:
            pass

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(socket_address)
        self.sock.listen(1)

        for _ in range(3):
            p = self.start_new_worker()
    
        def kill_workers():
            sys.stderr.write("server shutting down\n")
            sys.stderr.flush()
            for p in self.worker_pool:
                try:
                    os.kill(p.pid, signal.SIGKILL)
                except:
                    pass
            os.kill(os.getpid(), signal.SIGKILL)

        self.wd = Watchdog(SERVER_TIMEOUT_SECONDS, kill_workers)
        self.wd.start()

        sys.stdout.write("ready\n")
        sys.stdout.flush()

    def run(self):
        while True:
            try:
                # server waiting for client
                client_conn, client_address = self.sock.accept()
                self.wd.refresh()

                if self.available_workers.empty():
                    self.start_new_worker()
                worker_id = self.available_workers.get()
                worker_address = workerid_to_socket(worker_id)

                response = worker_address.encode()[:MAX_WORD_LEN].ljust(MAX_WORD_LEN, b"\0")

                client_conn.sendall(response)
            except Exception as e:
                print(e)

            finally:
                client_conn.close()

Daemon().run()
