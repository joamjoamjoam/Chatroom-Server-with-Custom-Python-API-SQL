import socket
import sys
import getpass
import os
import time
import cPickle as pickle
import cStringIO as StringIO
import Tkinter

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

def createChat(chatname):
    sock.send('createchat')
    time.sleep(.3)
    sock.send(chatname)
    tmp = sock.recv(4096)
    if tmp == 'YES':
        return True
    else:
        print 'Room name was taken. Pleas Choose another.'
        return False



def viewChats():
    sock.send('viewchats')
    chatIDs = pickle.loads(sock.recv(4096))

    return chatIDs

def deleteUser(userToDelete):
    sock.send('deleteuser')
    sock.send(userToDelete)
    response = sock.recv(4096)

    if response == 'YES':
        return True
    else:
        return False

def joinChat(chatname):
    sock.send('joinchat')
    time.sleep(.3)
    sock.send(chatname)

    if sock.recv(4096) == 'YES':
        return True
    else:
        return False

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
    login = Tkinter.Tk()
    top.mainloop()
