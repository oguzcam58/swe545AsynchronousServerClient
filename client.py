#!/usr/bin/env python
import socket # Import socket module
import threading # Import threading module
import Queue # Import Queue Module

# ------------------------Client------------------------
class Client:
	def __init__(self):
		self.clientSocket = socket.socket() # Create a socket object
		self.host = socket.gethostname() # Get local machine name
		self.port = 12345 # Reserve a port for your service.
	def connect(self):
		self.clientSocket.connect((self.host, self.port))
		while True:
			request = raw_input("Please enter what you want? ")
			self.clientSocket.send(request)
			while True:
				response = self.clientSocket.recv(1024)
				if response:
					print response
					break
		print "Exiting Client"
		# Quit
		self.clientSocket.close()

# ------------------------Main Program Functionality------------------------
client = Client()
client.connect()
