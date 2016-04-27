import socket
import sys
import getpass
import os
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('107.194.132.45', 7908)
print >>sys.stderr, 'connecting to %s port %s' % server_address
authenticationCredentials = ["",""]
choice = '0'
sock.connect(server_address)
authenticated = False

while choice == '0':

        print '1. Register'
        print '2. Login'
        print '3. Exit'
        choice = raw_input('Select an option > ')
        sock.send(choice)
        if choice == '1':
            choice = '0'
            done = False
            while not done:
                newName = raw_input('Username > ')
                sock.send(newName)
                newPass = raw_input('Password > ')
                sock.send(newPass)
                accepted = sock.recv(4096)
                if accepted == 'YES':
                    done = True
                else:
                    #username is taken
                    print('That username is taken. Please select a new one.')
        elif choice == '2':
            while not authenticated:
                #strip spaces from username
                authenticationCredentials[0] = raw_input('login_username:')
                authenticationCredentials[1] = getpass.getpass()

                #check credentials and disconnect if not correct
                sock.sendto(authenticationCredentials[0], server_address)
                sock.sendto(authenticationCredentials[1], server_address)

                authResponse = sock.recv(4096)

                if authResponse == 'NO':
                    print >> sys.stderr, 'Incorrect Credentials or You Are Logged in Somewhere Else'
                else:
                    print >> sys.stderr, 'Logged in Succesfully'
                    authenticated = True

        elif choice == '3':
            sock.close()
        else:
            print 'Invalid Choice. Please Choose Again'
            choice = '0'






sock.close()
print 'Succesfully Disconnected'
