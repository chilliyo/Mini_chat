#! python
#Qili Sui
# RecvMessages class
"""Relays messages between server and client."""
import threading
import os, sys


class RecvMessages(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        while True:
            try:
                msg_bytes = self.client_socket.recv(1024)
            except:  # socket was closed
                sys.exit()

            if len(msg_bytes):
                print(str(msg_bytes.decode()).strip('\n'))
            else:  # no bytes received; the other side shut down
                print('[other side shutdown; closing socket...]')
                self.client_socket.close()
                os._exit(0)