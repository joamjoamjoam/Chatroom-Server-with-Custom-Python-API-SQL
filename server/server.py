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
conn = ""

#create messages and get messages for chat
#edit profiles
#edit/ delete messages
#edit/delete chats

def serverFunctionalCode(connection, client_address):
    authenticated = False
    choice = '0'
    global connectedUser
    global cursor
    global DBcon
    global conn
    conn = connection
    #setup DB Connection
    try:
        DBcon = psycopg2.connect("dbname=mydb user=postgres password=cgttewr1 host=127.0.0.1 port=5433")
        DBcon.autocommit = True
        cursor = DBcon.cursor()
    except:
        print 'Couldnt connect to database'

    #menu 1 register or login or exit

    while 1:
        apiCall = connection.recv(4096)
        if apiCall == 'login':
            print 'Login request recieved from ', client_address
            login()
        elif apiCall == 'register':
            print 'Registering request recieved from ', client_address
            register()
        elif apiCall == 'viewfriendslist':
            print 'View Friends List request recieved from ', client_address
            print 'Connected User is %s' % connectedUser
            viewFriendsList()
        elif apiCall == 'createchat':
            print 'Create Chat request recieved from ', client_address
            print 'Connected User is %s' % connectedUser
            chatname = connection.recv(4096)
            createChat(chatname)
        elif apiCall == 'viewchats':
            print 'View Chats request recieved from ', client_address
            print 'Connected User is %s' % connectedUser
            viewChats()
        elif apiCall == 'addtofriendslist':
            print 'Add to Friends List request recieved from ', client_address
            print 'Connected User is %s' % connectedUser
            userToAdd = connection.recv(4096)
            addUserToFriendsList(userToAdd)
        elif apiCall == 'logout':
            print 'Logout request recieved from ', client_address
            logout()
        elif apiCall == 'deleteuser':
            print 'Delete User request request recieved from ', client_address
            user = connection.recv(4096)
            deleteuser(user)
        elif apiCall == 'joinchat':
            print 'join chat request request recieved from ', client_address
            chatname = connection.recv(4096)
            joinChat(chatname)
        elif apiCall == 'chatforname':
            print 'chatforname request request recieved from ', client_address
            chatname = connection.recv(4096)
            chatForName(chatname)
        elif apiCall == 'exit':
            print 'Exit request recieved from ', client_address
            connection.close()
            return 0
        else:
            print 'Invalid Call'

def register():
    global connectedUser
    global cursor
    global DBcon
    global conn

    newName = conn.recv(4096)
    newPass = conn.recv(4096)
    cursor.execute("SELECT login FROM usr WHERE login ='%s'" % newName)
    results = cursor.fetchall()
    if len(results) == 0:
        try:
            cursor.execute("INSERT INTO usrlist(owner) VALUES('%s') RETURNING list_id" % newName)
            listID = cursor.fetchone()[0]
            bio = "This is a bio."
            print 'listID = ', listID
            cursor.execute("INSERT INTO usr(login,password,bio,friendslist) VALUES ('%s','%s','%s',%d)" % (newName, newPass,bio,listID))
            conn.send('YES')
            print '%s succesfully registered' % newName
            DBcon.commit()
            connectedUser = newName
            authenticated = True
        except psycopg2.Error as e:
            print ("Error Inserting new user into usr table.")
            print e
            conn.send('NO')
    else:
        #username is taken
        conn.send('NO')
    connectedUser = newName


def login():
    global connectedUser
    global cursor
    global DBcon
    global conn
    tmpUser = conn.recv(4096)
    tmpPassword = conn.recv(4096)

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
        conn.send('YES')
    else:
        conn.send('NO')

def logout():
    global connectedUser
    connectedUser = ""

def viewFriendsList():
    global cursor
    global connectedUser
    global DBcon
    global conn
    try:
        cursor.execute("SELECT friendslist FROM usr WHERE login='%s'" % connectedUser)
        friendsListID = cursor.fetchone()[0]
        cursor.execute("SELECT member FROM usrlist_contains WHERE list_id=%d" %(friendsListID))
        results = cursor.fetchall()
        conn.send(pickle.dumps(results))
    except psycopg2.Error as e:
        print 'error viewing friendslist'
        print e

def addUserToFriendsList(userToAdd):
    global cursor
    global connectedUser
    global DBcon
    global conn
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
            conn.send("YES")
        except psycopg2.Error as e:
            print 'error adding to friendslist'
            print e
            conn.send("NO")
    else:
        conn.send('NO')

def createChat(chatname):
    global cursor
    global connectedUser
    global DBcon
    global conn

    try:
        cursor.execute("INSERT INTO chat(chatroom_name,initialsender) VALUES ('%s','%s')" % (chatname, connectedUser))
        cursor.execute("INSERT INTO chatlist VALUES ('%s','%s')" %(chatname, connectedUser))
        DBcon.commit()
        print 'Chat created with name', chatname, ' and initalsender ', connectedUser
        conn.send('YES')
    except psycopg2.Error as e:
        print 'Error creating chat.'
        print e
        conn.send('NO')



def viewChats():
    global cursor
    global connectedUser
    global DBcon
    global conn
    try:
        cursor.execute("SELECT chatroom_name FROM chatlist WHERE member='%s'" % connectedUser)
        results = cursor.fetchall()
        conn.send(pickle.dumps(results))
    except psycopg2.Error as e:
        print 'error viewing chatlist'
        print e

def deleteuser(user):
    global cursor
    global connectedUser
    global DBcon
    global conn
    if user == connectedUser:
        try:

            cursor.execute("DELETE FROM chatlist WHERE member='%s'" % connectedUser)
            cursor.execute("DELETE FROM message WHERE sender='%s'" % connectedUser)
            cursor.execute("SELECT chatroom_name FROM chat WHERE initialsender='%s'" % connectedUser)
            results = cursor.fetchall()
            # delete all from chatslist where usr is initial sender
            for tmp in results:
                cursor.execute("DELETE FROM chatlist WHERE chatroom_name='%s'" % results[0][0])


            cursor.execute("DELETE FROM chat WHERE initialsender='%s'" % connectedUser)
            cursor.execute("SELECT list_id FROM usrlist WHERE owner='%s'" % connectedUser)
            results = cursor.fetchall()
            listID = results[0][0]
            cursor.execute("DELETE FROM usr WHERE login='%s'" % connectedUser)
            cursor.execute("DELETE FROM usrlist_contains WHERE list_id=%d" % listID)
            cursor.execute("DELETE FROM usrlist_contains WHERE member='%s'" % connectedUser)
            cursor.execute("DELETE FROM usrlist WHERE owner='%s'" % connectedUser)
            time.sleep(.3)
            conn.send('YES')
        except psycopg2.Error as e:
            print 'error Deleting User'
            print e
            conn.send('NO')
    else:
        print 'trying to delete other user'
        conn.send('NO')

def joinChat(chatname):
    global cursor
    global connectedUser
    global DBcon
    global conn
    try:
        cursor.execute("SELECT chatroom_name FROM chat WHERE chatroom_name='%s'" % chatname)
        results = cursor.fetchall()
        if len(results) > 0 and results[0][0] == chatname:
            cursor.execute("INSERT INTO chatlist VALUES('%s','%s')" % (chatname, connectedUser))
            print 'Joined Succesufully'
            conn.send('YES')
        else:
            print 'no room with that name'
            conn.send('NO')

    except psycopg2.Error as e:
        print 'error viewing chatlist'
        print e
        conn.send('NO')

def chatForName(chatname):
    global cursor
    global connectedUser
    global DBcon
    global conn
    results = []
    try:
        cursor.execute("SELECT * FROM message WHERE chatroom_name='%s'" % chatname)
        results = cursor.fetchall()
        if len(results) > 0 and results[0][0] == chatname:
            conn.send(pickle.dumps(results))
        else:
            print 'no room with that name'
            conn.send(pickle.dumps(results))

    except psycopg2.Error as e:
        print 'error getting chatforname'
        print e
        conn.send(pickle.dumps(results))


if __name__=='__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 7908)
    #server_address = ('192.168.1.72', 7908)

    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)
    while 1:
        print 'waiting for connection...'
        connection, client_address = sock.accept()
        print '...connected from:', client_address
        thread.start_new_thread(serverFunctionalCode, (connection, client_address))
