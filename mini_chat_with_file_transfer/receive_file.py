#! python
# Qili Sui
# RecvFile class
"""Relays Files and File name between client and server."""
import threading
import os, sys

class RecvFile(threading.Thread):
    def __init__(self, second_socket):
        threading.Thread.__init__(self)
        self.second_socket = second_socket

    def run(self):
        while True:
            try:
                msg_bytes = self.second_socket.recv(102400)
            except:  # socket was closed
                sys.exit()
            if len(msg_bytes):
                try:
                    if msg_bytes.decode()[0:8] == "filename": #if receives a filename
                        filename = str(msg_bytes.decode()[8:].strip()+'\n')

                        try:
                            f = open(filename.strip(),'rb')
                            print("Received file reuqest: " + filename.strip(' \n'))
                            print("open " + filename.strip(' \n') + " successfully.")
                            file_content = f.read(102400)
                            self.second_socket.send(filename.encode()+file_content)
                            print("sent " + filename.strip(' \n') + " sccessfully.")
                            f.close()

                        except:
                            cantopen = "Can't open file OR the file doesn't exist."
                            self.second_socket.send(cantopen.encode())
                            
                    # if receives a can't open message
                    elif msg_bytes.decode()[0:15] == "Can't open file":
                            print(msg_bytes.decode())

                    else: #if receives file content.
                        fn_content = msg_bytes.decode('utf-8','replace').split('\n')
                        filename_rev_with_content = fn_content[0]


                        full_content = ""
                        for i in (range(1, len(fn_content))):
                            if fn_content[i] == '':
                                pass
                            else:
                                full_content = full_content + (fn_content[i] + '\n')

                        write_content = full_content.encode()

                        with open(filename_rev_with_content, 'wb') as file:
                            file.write(write_content)
                            print("You got a copy of " + filename_rev_with_content + ". Please check out your current directory.")

                except: #handle non-utf8 bytes
                    images_bytes = msg_bytes
                    images_str = images_bytes.decode('utf-8','replace')

                    got_file_name = images_str.split('\n')[0]
                    got_file_name_2 = images_str.split('\n')[0]+'\n'

                    filename_sub = got_file_name_2.encode()
                    content = msg_bytes.replace(filename_sub, b'')

                    f = open(got_file_name, 'wb')
                    f.write(content)
                    print("You got a copy of " + got_file_name + ".Please check out your current directory.")

            else:  # no bytes received; the other side shut down
                print('[other side shutdown; closing socket...]')
                self.second_socket.close()
                os._exit(0)