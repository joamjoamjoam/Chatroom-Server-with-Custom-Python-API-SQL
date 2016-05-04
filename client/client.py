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

def chatForName(chatname):
    sock.send('chatforname')
    time.sleep(.3)
    sock.send(chatname)

    results = pickle.loads(sock.recv(4096))

    return results


def createMessage(text,chatname):
    sock.send('createmessage')
    time.sleep(.3)
    sock.send(text)
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
    choice = '0'
    wantsToExit = False
    while not authenticated and not wantsToExit:
        while not authenticated or wantsToExit:
            print '1. Register'
            print '2. Login'
            print '3. Exit'
            choice = raw_input('Select an option > ')

            if choice == '1':
                user = raw_input('login_username:')
                password = getpass.getpass()
                authenticated = register(user, password)
                currentUser = user
            elif choice == '2':
                user = raw_input('Username > ')
                password = raw_input('Password > ')
                authenticated = login(user, password)
            elif choice == '3':
                disconnect()
                wantsToExit = True
                break
        choice = '0'
        while authenticated and choice == '0':
            print '1. Create Chat'
            print '2. View Chats'
            print '3. Add to Friends'
            print '4. View Friends List'
            print '5. Join Chat'
            print '6. Logout'
            print '7. Delete User'
            print '8. Exit'
            choice = raw_input('Select an option > ')

            if choice == '1':
                #create chat
                chatname = raw_input('Please input a chat room name >> ')
                if createChat(chatname):
                    print 'chat created succesfully'
                choice = '0'
            elif choice == '2':
                #view chat
                done = False
                done2 = False
                chats = viewChats()
                while not done:
                    for i in range(0,len(chats),1):
                        print i+1, '. ', chats[i][0]
                    tmp = raw_input('Enter 0 when done >> ')
                    if tmp == '0':
                        done = True
                    elif int(float(tmp)) > 0 and int(float(tmp)) <= len(chats):

                        while not done2:
                            messages = chatForName(chats[int(float(tmp)) - 1][0])
                            print messages
                            for i in range(0,len(messages),1):
                                print i+1, '. ', messages[i][1], messages[i][3], messages[i][2]
                            tmp = raw_input('Enter 0 when done or 1 to create message >> ')
                            if tmp == '0':
                                done = True
                            else:
                                text = raw_input('message text >> ')
                                createMessage(text,chats[int(float(tmp)) -1][0])
                choice = '0'
            elif choice == '3':
                #add to friends
                add = raw_input('User to add >> ')
                if addUserToFriendsList(add):
                    print 'User Added'
                else:
                    print 'No User with that name.'
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
                #join chat
                chatname = raw_input('Chat to Join >> ')
                if joinChat(chatname):
                    print 'Chat %s Joined' % chatname
                else:
                    print 'No Chat with that name'
                choice = '0'
            elif choice == '6':
                logout()
                authenticated = False
            elif choice == '7':
                if deleteUser(user):
                    authenticated = False
                    print 'User Was Deleted'
                else:
                    print 'You can only delete the currently logged in user'
                    choice == '0'
            elif choice == '8':
                disconnect()
                wantsToExit = True
                break
        choice = '0'
