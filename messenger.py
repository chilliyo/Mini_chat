import getopt
import sys
import socket
import threading,time
import os


# Four thread handling functions:
def usage( script_name ):
    print( 'Usage: python3 ' + script_name + ' <port number>' )
    # port number range:0-64k

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

if __name__ == "__main__":

    argc = len(sys.argv)
    # handle command line arguments
    # Exit immediately if num of argument is not 2 or 3
    if argc != 2 and argc != 3:
        usage(sys.argv[0])
        os._exit(0)
    try:
        opts,args = getopt.getopt(sys.argv[1:],'l:')

    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        os._exit(0)
    
    # Exit instruction for both server and client
    print('Press Ctrl + C to exit.')

    # Server Side
    if opts:
        flag = opts[0][0]
        port = opts[0][1]
        if flag == "-l":
            # create a communicator socket object
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serversocket.bind(('localhost', int(port)))
            serversocket.listen(5)

            #create a connection flag
            any_connection = False
            
            while True: 
                try:
                    sock, addr = serversocket.accept()
                    print("Accpeted 1 Client on port " + str(port))

                    # change connection flag to True after accpet a client
                    any_connection = True

                    thread_send = threading.Thread(target=send, args=[sock])
                    thread_recv = threading.Thread(target=receive, args=[sock])
                    thread_send.start()
                    thread_recv.start()

                except KeyboardInterrupt:
                    # ctrl + c to exit
                    print("You pressed Ctrl + C to exit.")

                    # send 0-length message to terminate the other side
                    # sock.send("".encode())
                    # print("Zero-length message sent.")
                    sock.shutdown(socket.SHUT_WR)
                    socket_close(sock)

    # Client Side
    if args != [] and sys.argv[1] != '-l':
        
        argc = len(sys.argv)
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

            #connect
            clientsocket.connect((server, int(port) ))
            print("Connected to "+ server + " at port " + str(port))

            thread_send = threading.Thread(target=send, args=[clientsocket])
            thread_recv = threading.Thread(target=receive, args=[clientsocket])
            thread_send.start()
            thread_recv.start()
            while True: time.sleep(100)
        # except ConnectionRefusedError:
        #     print("Can not find the server, connection refused.")
        except (KeyboardInterrupt,SystemExit):
            print("You pressed Ctrl + C to exit.")

            # close client socket
            clientsocket.shutdown(socket.SHUT_WR)
            socket_close(clientsocket)
            
    
        



