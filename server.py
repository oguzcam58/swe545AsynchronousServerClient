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

threadCounter = 0 # Give number to threads
serverThread = Server()
serverThread.start()