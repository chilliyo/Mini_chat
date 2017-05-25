'''
Qili Sui
MiniChat_with_FileTransfer
'''

import getopt
import sys
import socket
import threading
import os


global server_listen_port
server_listen_port = ''
global client_listen_port
client_listen_port = ''
global server
server = None

def connectToServer( port, server ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if server:
        sock.connect((server, int(port)))
    else:
        sock.connect(('localhost', int(port)))
    return sock
    
def listenForConnection( port ):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('', int(port)))
    serversocket.listen(5)
    sock, addr= serversocket.accept()
    return sock

def usage(script_name):
    print('Usage as a Server:')
    print('Usage: python3 ' + script_name + ' -l <listening port number>\n')
    print('Usage as a Client:')
    print('Usage: python3 ' + script_name + ' -l <listening port number> [-s] [connect server address] -l <connect server port>')
    # port number range:0-64k

def send(sock,message):
    if not message:
        return None
    try:
        sock.send(message.encode())
    except:
        return None
    return 1

def receive(sock):
    while True:
        msg_bytes = sock.recv(1024)
        message = str(msg_bytes.decode())
        client_listen_port = message
        return client_listen_port

def displayMenu():
    print("Enter an option ('m', 'f', 'x':)\n  (M)essage (send)\n  (F)ile (request)\ne(X)it")

def getOption():
    response = sys.stdin.readline()
    if not response:
        return None
    return response.strip(' \n')

def oops( server ):
    print( 'Oops! you specified both the listening flag (-1) and a server address (' + server + '), which is used only for a client. Please remove one of them.' )

if __name__ == "__main__":
    try:
        argc = len(sys.argv)
        # handle command line arguments
        # Exit immediately if num of argument is not 3 or 5 or 7
        if argc != 3 and argc != 7 and argc != 5:
            usage(sys.argv[0])
            os._exit(0)
        try:
            optlist, non_option_args= getopt.getopt( sys.argv[1:], 'l:s:p:' )
            act_as_server = False

            for opt,arg in optlist:
                if opt == '-l' and argc == 3:
                    server_listen_port = arg
                    act_as_server = True
                    print('listening on port ' + server_listen_port)
                elif opt == '-l' and argc == 5:
                    client_listen_port = arg
                    print('listening on port ' + client_listen_port)
                elif opt == '-p' and argc == 5:
                    server_listen_port = arg
                    print('connecting to localhost on port ' + server_listen_port)
                elif opt == '-l' and argc == 7:
                    client_listen_port = arg
                    print('listening on port ' + client_listen_port)
                elif opt == '-p' and argc == 7:
                    server_listen_port = arg
                    print('connecting to localhost on port ' + server_listen_port)
                elif opt == '-s' and argc == 7:
                    server = arg
                    print('connecting to ' + server + ' on port ' + server_listen_port)

        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            os._exit(0)

        #server for first socket
        if act_as_server:
            sock = listenForConnection(server_listen_port)

        #client
        else:
            sock = connectToServer (server_listen_port,server)
            send(sock, client_listen_port)
            second_sock = listenForConnection(client_listen_port)
            print("Second scoket connected on port " + client_listen_port)

        #server for second socket
        if act_as_server:
            client_listen_port = receive(sock)
            second_sock = connectToServer(client_listen_port, server)
            print('Second Socket connected on port ' + client_listen_port)
        else:
            pass

        from receive_message import RecvMessages
        RecvMessages(sock).start()
        from receive_file import RecvFile
        RecvFile(second_sock).start()

        while True:
            displayMenu()
            option = getOption()
            if not option:
                break
            if option == 'm':  # send a message
                print("Enter Your Message: ")
                message_from_other_side = sys.stdin.readline()
                if not send(sock,message_from_other_side):
                    break
            elif option == 'f':  # request a file transfer
               print("What file are you requesting?")
               file_name = sys.stdin.readline()
               sent_file_name = 'filename'+file_name
               print("Your request for "+ file_name.strip(' \n')+ " sent.")
               if not send(second_sock, sent_file_name):
                   break
            elif option == 'x':  # exit
                break
            else:  # ignore invalid choice
                pass
        try:
            sock.shutdown(socket.SHUT_WR)
            sock.close()

            second_sock.shutdown(socket.SHUT_WR)
            second_sock.close()
        except:
            pass

    except (KeyboardInterrupt, SystemExit):
        print("You pressed Ctrl + C to close standard input.")
        # close client socket
        sock.shutdown(socket.SHUT_WR)
        second_sock.shutdown(socket.SHUT_WR)
        sock.close()
        second_sock.close()







