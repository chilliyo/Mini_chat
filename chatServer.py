import sys
import socket
import threading,time
import os

CLINET_CONNECTION_LIST = []


def accpet_client(sock):
    sock, addr = serversocket.accept()
    print("Accpeted Client [" + str(addr) + "]on port " + str(port))
    return sock,addr

def send(sock,addr):
    while True:
        message = sys.stdin.readline()
        sock.send(message.encode())

def receive(sock,addr):
    while True:
        msg_bytes = sock.recv(1024)
        message = str(msg_bytes.decode())
        if message == "":
            some_client_disconnected = "Client" + str(addr) + "is disconnected now."
            print(some_client_disconnected)
            CLINET_CONNECTION_LIST.remove(sock)
            #socket_close(sock)
            break
        ready_broadcast = "[" + str(addr) + "]: " + str(msg_bytes.decode()).strip('\n')
        print(ready_broadcast)
        for socket in CLINET_CONNECTION_LIST:
            if socket != serversocket and socket != sock:
                try:
                    print("broadcasting...")
                    socket.send(ready_broadcast.encode())
                except:
                    socket.close()
                    CLINET_CONNECTION_LIST.remove(socket)

def socket_close(sock):
    sock.close()
    print("Connection closed.")
    os._exit(0)

def usage(script_name):
	print('Usage: python3 ' + script_name + '<port number>' + '[server address]' )

if __name__ == "__main__":
    #get the command line arguments
    argc = len (sys.argv)
    if argc != 2 and argc != 3:
        usage(sys.argv[0])
        os._exit(0)

    print ('Press Ctrl + C to exit.')

    port = sys.argv[1]

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', int(port)))
    serversocket.listen(5)
    #print (type(CLINET_CONNECTION_LIST[0]))
    # create a connection flag
    #any_connection = False

    while True:
        try:
            sock,addr = accpet_client(socket)
            CLINET_CONNECTION_LIST.append(sock)
            print ("Client (%s, %s) connected" % addr)
            print ("Total of %s Client(s) in this chat now." % len(CLINET_CONNECTION_LIST))

            thread_send = threading.Thread(target=send, args=[sock,addr])
            thread_recv = threading.Thread(target=receive, args=[sock,addr])
            thread_send.start()
            thread_recv.start()

        except (KeyboardInterrupt,SystemExit):
            # ctrl + c to exit
            print("You exit.")
            sock.shutdown(socket.SHUT_WR)
            socket_close(sock)

