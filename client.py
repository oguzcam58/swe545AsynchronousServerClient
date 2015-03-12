#!/usr/bin/env python
import socket # Import socket module
import threading # Import threading module

# ------------------------Client------------------------
class Client:
	threadCounter = 0 # Give number to threads
	def __init__(self):
		self.connection = socket.socket() # Create a socket object
		self.host = socket.gethostname() # Get local machine name
		self.port = 12345 # Reserve a port for your service.
	def connect(self):
		self.connection.connect((self.host, self.port))
		# ------------------------ReaderThread------------------------
		self.threadCounter += 1
		readerThread = ReaderThread(self.threadCounter, "Thread-" + str(self.threadCounter), self.connection)
		readerThread.start()
		# ------------------------WriterThread------------------------
		self.threadCounter += 1
		writerThread = WriterThread(self.threadCounter, "Thread-" + str(self.threadCounter), self.connection)
		writerThread.start()

# ------------------------ReaderThread------------------------
class ReaderThread(threading.Thread):
	def __init__(self, threadID, name, connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
	def run(self):
		global exitFlag
		global wait
		print("Starting ReaderThread " + str(self.threadID) + " " + self.name)
		while exitFlag:
			data = self.connection.recv(1024)
			if data:
				print(data)
				if data[0:3] == "BYE":
					exitFlag = False
				if data[0:3] == "NOW":
					self.connection.send("OK")
				wait = False

# ------------------------WriterThread------------------------
class WriterThread(threading.Thread):
	def __init__(self, threadID, name, connection):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
	def run(self):
		global exitFlag
		global wait
		print("Starting WriterThread " + str(self.threadID) + " " + self.name)
		while exitFlag:
			if not wait:
				request = raw_input("Please enter what you want? ")
				self.connection.send(request)
				wait = True

# ------------------------Main Program Functionality------------------------
exitFlag = True
wait = False
client = Client()
client.connect()
