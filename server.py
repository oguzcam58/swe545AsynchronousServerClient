#!/usr/bin/env python
import socket # Import socket module
import threading # Import threading module
import Queue # Import Queue Module
import time # Import Time Module

# ------------------------Server------------------------
class Server:
	serverSocket = socket.socket() # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12345 # Reserve a port for your service.
	def start(self):
		self.codes = dict()
		f = open("codes.txt", "r")
		for line in f:
			line = line.strip()
			splitresult = line.split(' ', 1)
			if len(splitresult) == 2:
				self.codes[splitresult[1]] = splitresult[0]
			else:
				raise Exception("Error in codes file!")
		f.close()
		print(self.codes)

		global threadCounter
		self.serverSocket.bind((self.host, self.port)) # Bind to the port
		self.serverSocket.listen(1000) # Now wait for client connection.
		print('Server socket is created and it is the listening mode on ' + self.host + ":" + str(self.port))
		while True:
			connection, address = self.serverSocket.accept() # Establish connection with client.
			print('Got connection from ', address)
			readerQueue = Queue.Queue(10)
			writerQueue = Queue.Queue(10)
			# ------------------------ReaderThread------------------------
			threadCounter += 1
			readerThread = ReaderThread(threadCounter, "Thread-" + str(threadCounter), connection, readerQueue)
			readerThread.start()
			# ------------------------WriterThread------------------------
			threadCounter += 1
			writerThread = WriterThread(threadCounter, "Thread-" + str(threadCounter), connection, writerQueue)
			writerThread.start()
			# ------------------------ParserThread------------------------
			threadCounter += 1
			parserThread = ParserThread(threadCounter, "Thread-" + str(threadCounter), connection, readerQueue, writerQueue, self.codes)
			parserThread.start()

# ------------------------ReaderThread------------------------
class ReaderThread(threading.Thread):
	def __init__(self, threadID, name, connection, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.queue = queue
	def run(self):
		print("Starting ReaderThread " + str(self.threadID) + " " + self.name)
		while True:
			data = self.connection.recv(1024)
			if not data:
				continue
			self.queue.put(data)

# ------------------------WriterThread------------------------
class WriterThread(threading.Thread):
	def __init__(self, threadID, name, connection, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.queue = queue
	def run(self):
		print("Starting WriterThread " + str(self.threadID) + " " + self.name)
		while True:
			print("Printing data got from client" + str(self.queue.get()))

# ------------------------WriterThread------------------------
class ParserThread(threading.Thread):
	def __init__(self, threadID, name, connection, readerQueue, writerQueue, codes):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.readerQueue = readerQueue
		self.writerQueue = writerQueue
		self.codes = codes
	def run(self):
		print("Starting ParserThread " + str(self.threadID) + " " + self.name)
		while True:
			data = self.readerQueue.get()
			if not (len(data) == 3 or (len(data) > 3 and data[3:4] == " ")):
				response = "ERR"
				self.connection.send(response)
			elif data[0:3] == "HEL":
				response = "SLT"
				self.connection.send(response)
			elif data[0:3] == "GET":
				country = data[4:]
				if self.codes.has_key(country):
					response = "CDE" + " " + self.codes[country]
				else:
					response = "NTF" + " " + country
				self.connection.send(response)
			elif data[0:3] == "TIC":
				response = "TOC" + " " + time.ctime(time.time())
				self.connection.send(response)
			elif data[0:3] == "QUI":
				response = "BYE"
				self.connection.send(response)
			else:
				response = "ERR"
				self.connection.send(response)

threadCounter = 0 # Give number to threads
serverThread = Server()
serverThread.start()