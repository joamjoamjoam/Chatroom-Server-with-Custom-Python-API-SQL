import socket
import sys
import getpass
import os
import time
import cPickle as pickle
import cStringIO as StringIO

sock = ""

def register(user, password):
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

def disconnect():
    sock.send('exit')
    sock.close()
    print 'Succesfully Disconnected'

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
    return result

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
    tmp = sock.recv(4096)
    if tmp == 'YES':
        return True
    else:
        return False



def viewChats():
    sock.send('viewchats')
    chatIDs = pickle.loads(sock.recv(4096))

    return chatIDs


if __name__=='__main__':
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
    while not authenticated and choice == '0':
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
                disconnect()

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
                if createChat():
                    print 'chat created succesfully'
                choice = '0'
            elif choice == '2':
                #view chat
                done = False
                chats = viewChats()
                print 'chats = ', chats
                while not done:
                    for i in range(0,len(chats),1):
                        print i+1, '. ', chats[i][0]
                    tmp = raw_input('Enter 0 when done >> ')
                    if tmp == '0':
                        done = True
                choice = '0'
            elif choice == '3':
                #add to friends
                add = raw_input('User to add >> ')
                addUserToFriendsList(add)
                choice = '0'
            elif choice == '4':
                #view friends list
                done = False
                friendsList = viewFriendsList()
                while not done:
                    for i in range(0,len(friendsList),1):
                        print i+1, '. ', friendsList[i][0]
                    tmp = raw_input('Enter 0 when done >> ')
                    if tmp == '0':
                        done = True
                choice = '0'
            elif choice == '5':
                logout()
                authenticated = False
            elif choice == '6':
                disconnect()
        choice = '0'
