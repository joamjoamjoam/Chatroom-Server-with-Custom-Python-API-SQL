import socket
import sys
import getpass
import os
import time
import cPickle as pickle
import cStringIO as StringIO
import htmlPy

sock = ""
globalusername = "NULL"

# Binding of back-end functionalities with GUI

class PythonAPI(htmlPy.Object):
	def __init__(self):
        	super(PythonAPI, self).__init__()

        	# Initialize the class here, if required.
        	return

	@htmlPy.Slot(str, str, result=str)
	def testAPI(self, argA, argB):
	    #just to test if the js is calling anything
	    print argA
	    print argB
	    return "hello!"

	@htmlPy.Slot(str, str, result=bool)
	def register(self, user, password):
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
	
	@htmlPy.Slot()
	def logout(self):
	    globalusername = "";
	    app.template = ("index2.html", {"dont_think_this": "matters"})
	    sock.send('logout')

	@htmlPy.Slot()
	def disconnect(self):
	    sock.send('exit')
	    sock.close()
	    print 'Succesfully Disconnected'

	@htmlPy.Slot(str, str, result=bool)
	def login(self, user, password):
	    global globalusername
	    sock.send('login')
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
		globalusername = user
		app.template = ("chatPage2.html", {"dont_think_this": "matters"})
		return True

	@htmlPy.Slot(result=str)
	def viewFriendsList(self):
	    sock.send("viewfriendslist")
	    #view friends list
	    pickledString = sock.recv(4096)
	    result = pickle.loads(pickledString)
	    return result

	@htmlPy.Slot(str, result=bool)
	def addUserToFriendsList(self, userToAdd):
	    sock.send("addtofriendslist")
	    sock.send(userToAdd)
	    accepted = sock.recv(4096)
	    if accepted == 'YES':
		return True
	    else:
		return False

	@htmlPy.Slot(str, result=bool)
	def createChat(self, chatname):
	    sock.send('createchat')
	    time.sleep(.3)
	    sock.send(chatname)
	    tmp = sock.recv(4096)
	    if tmp == 'YES':
		return True
	    else:
		print 'Room name was taken. Pleas Choose another.'
		return False



	@htmlPy.Slot(result=str)
	def viewChats(self):
	    sock.send('viewchats')
	    chatIDs = pickle.loads(sock.recv(4096))
	    return chatIDs

	@htmlPy.Slot(str, result=bool)
	def deleteUser(self, userToDelete):
	    sock.send('deleteuser')
	    sock.send(userToDelete)
	    response = sock.recv(4096)
	    if response == 'YES':
		return True
	    else:
		return False

	@htmlPy.Slot(str, result=bool)
	def joinChat(self, chatname):
	    sock.send('joinchat')
	    time.sleep(.3)
	    sock.send(chatname)

	    if sock.recv(4096) == 'YES':
		return True
	    else:
		return False

	@htmlPy.Slot(str, result=str)
	def chatForName(self, chatname):
		
	    sock.send('chatforname')
	    time.sleep(.3)
	    sock.send(chatname)

	    results = pickle.loads(sock.recv(4096))
	    return results


	@htmlPy.Slot(str, str, result=bool)
	def createMessage(self,text,chatname):
	    sock.send('createmessage')
	    time.sleep(.3)
	    sock.send(text)
	    sock.send(chatname)

	    if sock.recv(4096) == 'YES':
		return True
	    else:
		return False

	@htmlPy.Slot(result=str)
	def getUsername(self):
		return globalusername


#GUI STUFF ----------------------------------------------------------------------
# Initial confiurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# GUI initializations
app = htmlPy.AppGUI(title=u"Application", maximized=True, plugins=True)


# GUI configurations
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.web_app.setMinimumWidth(500)
app.web_app.setMinimumHeight(700)
app.template = ("index2.html", {"dont_think_this": "matters"})
app.bind(PythonAPI())
#GUI STUFF ----------------------------------------------------------------------

if __name__=='__main__':
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect the socket to the port where the server is listening
	#server_address = ('107.194.132.45', 7908)
	server_address = ('localhost', 7908)
	print >>sys.stderr, 'connecting to %s port %s' % server_address
	authenticationCredentials = ["",""]
        sock.connect(server_address)
   	app.start()
