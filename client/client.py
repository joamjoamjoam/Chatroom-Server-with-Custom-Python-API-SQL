import socket
import sys
import getpass
import os
import time
import cPickle as pickle
import cStringIO as StringIO

sock = ""

def register(user, password):
    global sock
    sock.send('register')
    sock.send(user)
    time.sleep(.3)
    sock.send(password)
    accepted = sock.recv(4096)
    if accepted == 'YES':
        return True
    else:
        #username is taken
        print('That username is taken. Please select a new one.')
        return False

def logout():
    sock.send('logout')

def login(user, password):
    sock.send("login")
    #check credentials and disconnect if not correct
    sock.sendto(user, server_address)
    time.sleep(.3)
    sock.sendto(password, server_address)

    authResponse = sock.recv(4096)

    if authResponse == 'NO':
        print >> sys.stderr, 'Incorrect Credentials or You Are Logged in Somewhere Else'
        return False
    else:
        print >> sys.stderr, 'Logged in Succesfully'
        return True


def viewFriendsList():
    sock.send("viewfriendslist")
    #view friends list
    pickledString = sock.recv(4096)
    result = pickle.loads(pickledString)
    for i in range(0,len(result),1):
        print i+1, '. ', result[i][0]
    done = raw_input('Enter 0 when done >> ')
    sock.send(done)

def addUserToFriendsList(userToAdd):
    sock.send("addtofriendslist")
    sock.send(userToAdd)
    accepted = sock.recv(4096)
    if accepted == 'YES':
        return True
    else:
        return False

def createChat():
    sock.send('createchat')
    global cursor
    global connectedUser
    global DBcon



def viewChat():
    sock.send('viewchats')
    global cursor
    global connectedUser
    global DBcon

if __name__=='__main__':
    global sock
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #server_address = ('107.194.132.45', 7908)
    server_address = ('192.168.1.72', 7908)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    authenticationCredentials = ["",""]
    sock.connect(server_address)
    authenticated = False
    choice = '0'
    while not authenticated && choice == '0':
        while not authenticated:
            print '1. Register'
            print '2. Login'
            print '3. Exit'
            choice = raw_input('Select an option > ')

            if choice == '1':
                user = raw_input('login_username:')
                password = getpass.getpass()
                authenticated = register(user, password)
            elif choice == '2':
                user = raw_input('Username > ')
                password = raw_input('Password > ')
                authenticated = login(user, password)
            elif choice == '3':
                sock.close()

        choice = '0'
        while choice == '0':
            print '1. Create Chat'
            print '2. View Chats'
            print '3. Add to Friends'
            print '4. View Friends List'
            print '5. Logout'
            print '6. Exit'
            choice = raw_input('Select an option > ')

            if choice == '1':
                #create chat
                print ''
            elif choice == '2':
                #view chat
                print ''
            elif choice == '3':
                #add to friends
                add = raw_input('User to add >> ')
                addUserToFriendsList(add)
                choice = '0'
            elif choice == '4':
                #view friends list
                friendsList = viewFriendsList()
                choice = '0'
            elif choice == '5':
                logout()
                authenticated = False
                choice = '0'

            elif choice == '6':
                sock.close()



    sock.close()
    print 'Succesfully Disconnected'
