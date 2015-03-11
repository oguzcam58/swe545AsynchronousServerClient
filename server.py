#!/usr/bin/env python
import socket # Import socket module
import threading # Import threading module

# ------------------------Server------------------------
class Server:
	serverSocket = socket.socket() # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12345 # Reserve a port for your service.
	def start(self):
		self.serverSocket.bind((self.host, self.port)) # Bind to the port
		self.serverSocket.listen(1000) # Now wait for client connection.
		print('Server socket is created and it is the listening mode on ' + self.host + ":" + str(self.port))
		while True:
			connection, address = self.serverSocket.accept() # Establish connection with client.
			print('Got connection from ', address)
			# ------------------------ReaderThread------------------------
			readerThread = ReaderThread(++threadCounter, "Thread-" + str(threadCounter), connection)
			readerThread.start()
			# ------------------------WriterThread------------------------
			writerThread = WriterThread(++threadCounter, "Thread-" + str(threadCounter), connection)
			writerThread.start()

# ------------------------ReaderThread------------------------
class ReaderThread(threading.Thread):
	def __init__(self, threadID, name, connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
	def run(self):
		print("Starting ReaderThread " + str(self.threadID) + " " + self.name)

# ------------------------WriterThread------------------------
class WriterThread(threading.Thread):
	def __init__(self, threadID, name, connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
	def run(self):
		print("Starting WriterThread " + str(self.threadID) + " " + self.name)

threadCounter = 0 # Give number to threads
serverThread = Server()
serverThread.start()