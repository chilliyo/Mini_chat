#! python

# RecvMessages class
"""Relays messages between clients."""
import threading
import os, sys


class RecvMessages(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    # def displayQnA(self, message):
    #     number, text = self.extract(message)
    #     i_number = int(number)
    #     question = self.my_questions[i_number]
    #     if question:
    #         print('Q: ' + question)
    #         print('   A: ' + text)
    #         self.my_questions.pop(i_number)
    #
    # def extract(self, message):
    #     second_colon = message.rfind(':')
    #     number = message[2:second_colon]
    #     text = message[second_colon + 1:]
    #     return (number, text)

    # def storeQuestion(self, message):
    #     number, text = self.extract(message)
    #     # add their question to the list
    #     self.their_questions[number] = text
    #     print('Q: ' + text)

    def run(self):
        while True:
            try:
                msg_bytes = self.client_socket.recv(1024)
            except:  # socket was closed
                sys.exit()
            if len(msg_bytes):
                print(str(msg_bytes.decode()).strip('\n'))
                # # determine whether message is a question or an answer
                # # if it is a question, add it to the pending list
                # if message[0] == 'q':
                #     self.storeQuestion(message)
                # elif message[0] == 'a':
                #     # if it is an answer, print both the original question and the answer
                #     self.displayQnA(message)
                    # print( msg_bytes.decode(), end= '' )
            else:  # no bytes received; the other side shut down
                print('[other side shutdown; closing socket...]')
                self.client_socket.close()
                os._exit(0)