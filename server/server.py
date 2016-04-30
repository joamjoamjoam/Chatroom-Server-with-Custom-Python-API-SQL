import socket
import sys
import thread
import time
import psycopg2
import cPickle as pickle
import cStringIO as StringIO

connectedUser = ""
cursor = ""
DBcon = ""

def serverFunctionalCode(connection, client_address):
    authenticated = False
    choice = '0'
    global connectedUser
    global cursor
    global DBcon
    #setup DB Connection
    try:
        DBcon = psycopg2.connect("dbname=mydb user=postgres password=cgttewr1 host=127.0.0.1 port=5433")
        cursor = DBcon.cursor()
    except:
        print 'Couldnt connect to database'

    #menu 1 register or login or exit

    while 1:
        apiCall = connection.recv(4096)
        if apiCall == 'login':
            login()
        elif 'register':
            print 'Registering request recieved from %s' % client_address
            register()
        elif apiCall == 'viewfriendslist':
            print 'View Friends List request recieved from %s' % client_address
            print 'Connected User is %s' % connectedUser
            viewFriendsList()
        elif apiCall == 'createchat':
            print 'Create Chat request recieved from %s' % client_address
            print 'Connected User is %s' % connectedUser
            createChat()
        elif apiCall == 'viewchats':
            print 'View Chats request recieved from %s' % client_address
            print 'Connected User is %s' % connectedUser
            viewChats()
        elif apiCall == 'addtofriendslist':
            print 'Add to Friends List request recieved from %s' % client_address
            print 'Connected User is %s' % connectedUser
            userToAdd = connection.recv(4096)
            addUserToFriendsList(userToAdd)
        else:
            print 'Invalid Call'

def register():
    global connectedUser
    global cursor
    global DBcon

    newName = connection.recv(4096)
    newPass = connection.recv(4096)
    cursor.execute("SELECT login FROM usr WHERE login ='%s'" % newName)
    results = cursor.fetchall()
    if len(results) == 0:
        try:
            cursor.execute("INSERT INTO usrlist(owner) VALUES('%s') RETURNING list_id" % newName)
            listID = cursor.fetchone()[0]
            bio = "This is a bio."
            print 'listID = ', listID
            cursor.execute("INSERT INTO usr(login,password,bio,friendslist) VALUES ('%s','%s','%s',%d)" % (newName, newPass,bio,listID))
            connection.send('YES')
            print '%s succesfully registered' % newName
            DBcon.commit()
            connectedUser = newName
            authenticated = True
        except psycopg2.Error as e:
            print ("Error Inserting new user into usr table.")
            print e
            connection.send('NO')
    else:
        #username is taken
        connection.send('NO')
    connectedUser = newName


def login():
    global connectedUser
    global cursor
    global DBcon
    tmpUser = connection.recv(4096)
    tmpPassword = connection.recv(4096)

    #validate credentials and set authenticated
    try:
        cursor.execute("SELECT password FROM usr WHERE login ='%s'" % tmpUser)
        results = cursor.fetchall()
    except psycopg2.Error as e:
        print 'error running select query for login'
        print e
    if len(results) > 0 and results[0][0] == tmpPassword:
        authenticated = True
        connectedUser = tmpUser
        connection.send('YES')
    else:
        connection.send('NO')


def viewFriendsList():
    global cursor
    global connectedUser
    global DBcon
    done = False
    while not done:
        try:
            cursor.execute("SELECT friendslist FROM usr WHERE login='%s'" % connectedUser)
            friendsListID = cursor.fetchone()[0]
            cursor.execute("SELECT member FROM usrlist_contains WHERE list_id=%d" %(friendsListID))
            results = cursor.fetchall()
            connection.send(pickle.dumps(results))
            DBcon.commit()
        except psycopg2.Error as e:
            print 'error adding to friendslist'
            print e
        if connection.recv(4096) == '0':
            done = True

def addUserToFriendsList(userToAdd):
    global cursor
    global connectedUser
    global DBcon
    results = []
    try:
        cursor.execute("SELECT login FROM usr WHERE login ='%s'" % userToAdd)
        results = cursor.fetchall()
    except psycopg2.Error as e:
        print 'error finding user to add to friends list'
        print e

    if len(results) > 0:
        # add user
        try:
            cursor.execute("SELECT friendslist FROM usr WHERE login='%s'" % connectedUser)
            friendsListID = cursor.fetchone()[0]
            cursor.execute("INSERT INTO usrlist_contains(list_id,member) VALUES (%d,'%s')" %(friendsListID, userToAdd))
            DBcon.commit()
        except psycopg2.Error as e:
            print 'error adding to friendslist'
            print e

def createChat():
    global cursor
    global connectedUser
    global DBcon



def viewChat():
    global cursor
    global connectedUser
    global DBcon



if __name__=='__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    #server_address = ('0.0.0.0', 7908)
    server_address = ('192.168.1.72', 7908)

    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)
    while 1:
        print 'waiting for connection...'
        connection, client_address = sock.accept()
        print '...connected from:', client_address
        thread.start_new_thread(serverFunctionalCode, (connection, client_address))
