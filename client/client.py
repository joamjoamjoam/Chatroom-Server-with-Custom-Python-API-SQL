import socket
import sys
import getpass
import os
import time
import cPickle as pickle
import cStringIO as StringIO

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
            #strip spaces from username
            authenticationCredentials[0] = raw_input('login_username:')
            authenticationCredentials[1] = getpass.getpass()

            #check credentials and disconnect if not correct
            sock.sendto(authenticationCredentials[0], server_address)
            sock.sendto(authenticationCredentials[1], server_address)

            authResponse = sock.recv(4096)

            if authResponse == 'NO':
                print >> sys.stderr, 'Incorrect Credentials or You Are Logged in Somewhere Else'
                choice = '0'
            else:
                print >> sys.stderr, 'Logged in Succesfully'
                authenticated = True

        elif choice == '3':
            sock.close()
        else:
            print 'Invalid Choice. Please Choose Again'
            choice = '0'


choice = '0'
while choice == '0':
    print '1. Create Chat'
    print '2. View Chats'
    print '3. Add to Friends'
    print '4. View Friends List'
    print '5. Exit'
    choice = raw_input('Select an option > ')
    sock.send(choice)

    if choice == '1':
        #create chat
        print ''
    elif choice == '2':
        #view chat
        print ''
    elif choice == '3':
        #add to friends
        userToAdd = raw_input('Enter the user to add >> ')
        sock.send(userToAdd)
        choice = '0'
    elif choice == '4':
        #view friends list
        pickledString = sock.recv(4096)
        result = pickle.loads(pickledString)
        print result
        done = raw_input('Enter 0 when done >> ')
        sock.send(done)
        choice = '0'
        #unpickle string here
    elif choice == '5':
        #exit
        sock.close()






sock.close()
print 'Succesfully Disconnected'
