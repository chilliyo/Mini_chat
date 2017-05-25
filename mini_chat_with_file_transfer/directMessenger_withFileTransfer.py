'''
Qili Sui
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

# Four thread handling functions:
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
    # try:
    #     f = open(file_name.strip(),'rb')
    #     print("open successfully.")
    #     file_content = f.read(1024)
    #     second_sock.send(file_name.encode()+file_content)
    #     f.close()
    # except:
    #     return None
    # return 1
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
        # Exit immediately if num of argument is not 2 or 3
        if argc != 3 and argc != 7 and argc != 5:
            usage(sys.argv[0])
            os._exit(0)
        try:
            optlist, non_option_args= getopt.getopt( sys.argv[1:], 'l:s:p:' )
            act_as_server = False
            #print (optlist)
            #print(non_option_args)

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
            # for opt, arg in optlist:
            #     if opt == '-l':
            #         act_as_server= True
            # host_args_len= len(non_option_args)
            # port= non_option_args[0]
            # server = None

        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            os._exit(0)

        # store server address, if present
        # if host_args_len == 2:
        #     server = non_option_args[1]
        # if act_as_server == True and server:
        #     oops( server );
        #     sys.exit()
        # if act_as_server == True:
        #     print( 'listening on port ' + port )
        # elif server == None:
        #     print( 'connecting to localhost on port ' + port )
        # else:
        #     print( 'connecting to ' + server + ' on port ' + port )

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

               # # create a connection flag
                # any_connection = False
                # message_from_server = ""
                # while True:
                #     sock, addr = serversocket.accept()
                #     print("Accpeted 1 Client on port " + str(port))
                #     # while True:
                #     #     MorF = sys.stdin.readline()
                #     #     if MorF[0] == "M":
                #     #         break
                #     #     elif MorF[0] == "F":
                #     #         print("We are going to do file transfer!! Isn't that cool?")
                #     #         print("We are going to do message!! Isn't that cool?")

                #     # change connection flag to True after accpet a client
                #     any_connection = True

        #from file_request_listener import request_listener
        #file_name = ''
        #thread_request_listener = threading.Thread(target=file_transfer_request,args =[second_sock,file_name])
        # thread_send = threading.Thread(target=send, args=[sock,message])

        # thread_two_send.start()
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
            else:  # invalid choice
                pass
        try:
            sock.shutdown(socket.SHUT_WR)
            sock.close()

            second_sock.shutdown(socket.SHUT_WR)
            second_sock.close()
        except:
            pass
                # except KeyboardInterrupt:
                #     # ctrl + c to exit
                #     print("You pressed Ctrl + C to exit.")
                #
                #     # send 0-length message to terminate the other side
                #     # sock.send("".encode())
                #     # print("Zero-length message sent.")
                #     sock.shutdown(socket.SHUT_WR)
                #     socket_close(sock)

    # Client Side
    # if args != [] and sys.argv[1] != '-l':

    #     argc = len(sys.argv)
    #     if argc < 2:
    #         usage(sys.argv[0])
    #         os._exit(0)
    #     elif argc == 3:
    #         server = sys.argv[2]
    #     else:
    #         server = 'localhost'

    #     port = sys.argv[1]
    #     message_from_client = ""
    #     #try:
    #     # create a socket object
        
    #     clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     # connect
    #     clientsocket.connect((server, int(port)))
    #     # MorF = sys.stdin.readline()
    #     #
    #     # if MorF[0] == "M":
    #     #     print("We are going to do message!! Isn't that cool?")
    #     # elif MorF[0] == "F":
    #     #     print("We are going to do file transfer!! Isn't that cool?")
    #     thread_send = threading.Thread(target=send, args=[clientsocket,message_from_client])
    #     thread_recv = threading.Thread(target=receive, args=[clientsocket])
    #     thread_send.start()
    #     thread_recv.start()
    #     while True:
    #         displayMenu()
    #         option = getOption()
    #         if not option:
    #             break
    #         if option == 'm':  # ask a question
    #             print("Enter Your Message: ")
    #             message_from_client = sys.stdin.readline()
    #             if not send(clientsocket,message_from_client):
    #                 break
    #         elif option == 'f':  # answer a question
    #             print("file Transfer.")
    #         elif option == 'x':  # exit
    #             break
    #         else:  # invalid choice
    #             pass
    #     try:
    #         clientsocket.shutdown(socket.SHUT_WR)
    #         clientsocket.close()
    #     except:
    #         pass
    #         #while True: time.sleep(100)

    #         # loop to send messages

    #     # except ConnectionRefusedError:
    #     #     print("Can not find the server, connection refused.")
    except (KeyboardInterrupt, SystemExit):
        print("You pressed Ctrl + C to close standard input.")
        # close client socket
        sock.shutdown(socket.SHUT_WR)
        second_sock.shutdown(socket.SHUT_WR)
        sock.close()
        second_sock.close()







