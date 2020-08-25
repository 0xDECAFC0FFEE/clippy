#! /usr/bin/python
"""
Server to 
"""

SERVER_TIMEOUT_SECONDS = 20
server_address = './Alfred_Dictionary_Socket'
MAX_WORD_LEN = 256
MAX_DEF_LEN = 2048

if __name__ == "__main__":
    import socket
    import os
    from Watchdog import Watchdog 
    import sys
    from urllib3 import HTTPConnectionPool

    wd = Watchdog(SERVER_TIMEOUT_SECONDS) # time out server after a given amount of time
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
    sys.stdout.write("ready\n")
    sys.stdout.flush()

    # connecting to datamuse server
    datamuse_conn = HTTPConnectionPool("api.datamuse.com")

    while True:
        try:
            # server waiting for client
            client_conn, client_address = sock.accept()
            while True:
                # refresh inactivity watchdog
                wd.refresh()

                # recieve word.
                query = client_conn.recv(MAX_WORD_LEN)
                query = query.strip(b"\0").decode()

                if not query:
                    break
                
                response = datamuse_conn.urlopen('GET', f'/words?{query}')
                response = response.data[:MAX_DEF_LEN].ljust(MAX_DEF_LEN, b"\0")

                client_conn.sendall(response)
        except Exception as e:
            print(e)

        finally:
            client_conn.close()
