import multiprocessing as mp
import os
from config import SERVER_TIMEOUT_SECONDS, socket_address, MAX_WORD_LEN, MAX_DEF_LEN
import socket
from urllib3 import HTTPConnectionPool

def workerid_to_socket(worker_id: int) -> str:
    return f"{socket_address}_{worker_id}"

class Worker(mp.Process):
    """
        worker process that handles a client and holds a http connection to reuse
    """
    def __init__(self, worker_id: int, available_workers: mp.Queue):
        mp.Process.__init__(self)
        self.available_workers = available_workers
        self.worker_id = worker_id

        try:
            os.remove(workerid_to_socket(worker_id))
        except:
            pass

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(workerid_to_socket(worker_id))
        self.sock.listen(1)

        self.datamuse_conn = HTTPConnectionPool("api.datamuse.com")


    def run(self):
        while True:
            self.available_workers.put(self.worker_id)
            try:
                client_conn, client_address = self.sock.accept()
                # recieve word.
                query = client_conn.recv(MAX_WORD_LEN)
                query = query.strip(b"\0").decode()

                if not query:
                    break

                response = self.datamuse_conn.urlopen('GET', f'/words?{query}')

                padded_response = response.data[:MAX_DEF_LEN].ljust(MAX_DEF_LEN, b"\0")

                client_conn.sendall(padded_response)
            except Exception as e:
                pass
