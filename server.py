#!/usr/bin/env python
import socket # Import socket module
import threading # Import threading module
import Queue # Import Queue Module
import time # Import Time Module
from time import sleep # Import Sleep Function
from random import randint # Import RandomInt Function
import os

# ------------------------Server------------------------
class Server:
	serverSocket = socket.socket() # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12345 # Reserve a port for your service.
	threadCounter = 0 # Give number to threads
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
		# ------------------------ServerThread------------------------
		self.threadCounter += 1
		self.serverThread = ServerThread(self.threadCounter, "Thread-" + str(self.threadCounter))
		self.serverThread.start()
		# ------------------------LoggerThread------------------------
		self.threadCounter += 1
		self.loggerThread = LoggerThread(self.threadCounter, "Thread-" + str(self.threadCounter))
		self.loggerThread.start()

		self.serverSocket.bind((self.host, self.port)) # Bind to the port
		self.serverSocket.listen(1000) # Now wait for client connection.
		print('Server socket is created and it is the listening mode on ' + self.host + ":" + str(self.port))
		while not exitFlag:
			connection, address = self.serverSocket.accept() # Establish connection with client.
			log(address, self.port, "Got connection")
			readerQueue = Queue.Queue(10)
			# ------------------------ReaderThread------------------------
			self.threadCounter += 1
			readerThread = ReaderThread(self.threadCounter, "Thread-" + str(self.threadCounter), connection, address, self.port, readerQueue)
			readerThread.start()
			# ------------------------WriterThread------------------------
			self.threadCounter += 1
			writerThread = WriterThread(self.threadCounter, "Thread-" + str(self.threadCounter), connection, address, self.port)
			writerThread.start()
			# ------------------------ParserThread------------------------
			self.threadCounter += 1
			parserThread = ParserThread(self.threadCounter, "Thread-" + str(self.threadCounter), connection, address, self.port, self.codes, readerQueue)
			parserThread.start()

# ------------------------ReaderThread------------------------
class ReaderThread(threading.Thread):
	def __init__(self, threadID, name, connection, address, port, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.address = address
		self.port = port
		self.queue = queue
	def run(self):
		print("Starting ReaderThread " + str(self.threadID) + " " + self.name)
		while not exitFlag:
			try:
				data = self.connection.recv(1024)
				if not data:
					continue
				else:
					log(self.address, self.port, "Data received as " + data)
				if data == "TNX":
					continue
				self.queue.put(data)
			except:
				break

# ------------------------WriterThread------------------------
class WriterThread(threading.Thread):
	def __init__(self, threadID, name, connection, address, port):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.address = address
		self.port = port
	def run(self):
		print("Starting WriterThread " + str(self.threadID) + " " + self.name)
		while not exitFlag:
			sleep(randint(10, 100))
			try:
				sendTime = time.ctime(time.time())
				self.connection.send("NOW" + " " + sendTime)
				log(self.address, self.port, "Sent time to Client as " + sendTime)
			except:
				break

# ------------------------ParserThread------------------------
class ParserThread(threading.Thread):
	def __init__(self, threadID, name, connection, address, port, codes, readerQueue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.connection = connection
		self.address = address
		self.port = port
		self.codes = codes
		self.readerQueue = readerQueue
	def run(self):
		print("Starting ParserThread " + str(self.threadID) + " " + self.name)
		while not exitFlag:
			data = self.readerQueue.get()
			response = ""
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
			log(self.address, self.port, "Response sent to client as " + response)

# ------------------------LoggerThread------------------------
class LoggerThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		global loggerQueue
		print("Starting LoggerThread " + str(self.threadID) + " " + self.name)
		f = open("log.txt", "a+")
		while not exitFlag:
			f.write(loggerQueue.get())
			f.flush()
			os.fsync(f)
		f.close()

# ------------------------ServerThread------------------------
class ServerThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		global exitFlag
		print("Starting ServerThread " + str(self.threadID) + " " + self.name)
		entry = raw_input("Write 'EXIT' to stop server ")
		if entry == "EXIT":
			log(None, None, "Server is halted by admin")
			exitFlag = True

# ------------------------Main Program Functionality------------------------
loggerQueue = Queue.Queue(10)
exitFlag = False
def log(address, port, msg):
	loggerQueue.put(time.ctime(time.time()) + ":" + str(address) + ":" + str(port) + ":" + msg + "\n")

serverThread = Server()
serverThread.start()