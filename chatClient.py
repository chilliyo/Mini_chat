import sys
import socket
import threading,time
import os

socket_lst = []

def send(sock):
    while True:
        message = sys.stdin.readline()
        sock.send(message.encode())

def receive(sock):
    while True:
        msg_bytes = sock.recv(1024)
        message = str(msg_bytes.decode())
        if message == "":
            print("Received a zero-length message, connection will be terminated.")
            socket_close(sock)
            break
        print(str(msg_bytes.decode()).strip('\n'))

def socket_close(sock):
    sock.close()
    print("Connection closed.")
    os._exit(0)

def usage(script_name):
	print('Usage: python3 ' + script_name + '<port number>' + '[server address]' )

if __name__ == "__main__":
    #get the command line arguments
    argc = len (sys.argv)
    if argc < 2:
        usage(sys.argv[0])
        os._exit(0)
    elif argc == 3:
        server = sys.argv[2]
    else:
        server = 'localhost'

    port = sys.argv[1]

    try:
        # create a socket object
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # connect
            clientsocket.connect((server, int(port)))
            print("Connected to " + server + " at port " + str(port))
        except:
            print ('Unable to connect')
            sys.exit()
        while 1:
            socket_lst = [sys.stdin, clientsocket]
            for sock in socket_lst:
                if sock == clientsocket:
                    thread_recv = threading.Thread(target=receive, args=[clientsocket])
                    thread_recv.start()
                    thread_send = threading.Thread(target=send, args=[clientsocket])
                    thread_send.start()
                    time.sleep(100)

    except (KeyboardInterrupt, SystemExit):
        print("You pressed Ctrl + C to exit.")

        # close client socket
        clientsocket.shutdown(socket.SHUT_WR)
        socket_close(clientsocket)
