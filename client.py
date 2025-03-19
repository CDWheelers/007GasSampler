# Import socket module 
import socket             
from datetime import datetime
import time
import os
from collections import deque

# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 65432               
 
# connect to the server on local computer 
s.connect(('192.168.1.181', port)) 
 
# receive data from the server and decoding to get the string.

#s.send('get_data\n'.encode('utf-8'))
#print (s.recv(1024).decode('utf-8'))
# close the connection
# s.send('get_data_after[2025-03-09][22:47:11.63]\n'.encode('utf-8'))

filename = "data_local.txt" # For testing purposes

def most_recent():
	print(f"Gathering most recent data")
	def get_last_line(filepath):
		with open(filepath, 'r') as f:
			last_line = deque(f, maxlen=1).pop().strip()
		return last_line
			
	# last_line = get_last_line('data_local.txt')
	# print(last_line)
		
	# date = last_line[0:10]
	# time = last_line[11:22]
		
	# cmd = 'get_data_after['+date+']['+time+']\n'
	
	# s.send(cmd.encode('utf-8'))

	with open(filename, 'a') as file: #'w' overwrites file of same filename, 'a' appends
		try:
			s.settimeout(2)
		
			while True:
				
				last_line = get_last_line('data_local.txt')
				date = last_line[0:10]
				time = last_line[11:22]
		
				cmd = 'get_data_after['+date+']['+time+']\n'
	
				s.send(cmd.encode('utf-8'))
				
				data = s.recv(34) #recieve 34 bits at a time, since each entry in data.txt is 34 bits long
					
				if not data or data == b'get_data\n':  # Prevent writing the command to file
					break
						
				print(f"Writing to '{filename}'\n")
				file.write(data.decode('utf-8'))
				file.flush()  # Ensure immediate writing to the file from program buffer
				file.close
		except socket.timeout:
			print("No new data received")
			
if (os.path.exists("data_local.txt") == 0):
	print(f"File DNE, gathering data")

	s.sendall(b'get_data\n')
	
	with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
		while True:
			data = s.recv(34) #recieve 34 bits at a time, since each entry in data.txt is 34 bits long
			
			if not data or data == b'get_data\n':  # Prevent writing the command to file
				break
				
			# print(f"Writing to '{filename}'\n")
			file.write(data.decode('utf-8'))
			file.flush()  # Ensure immediate writing to the file from program buffer
 
elif (os.stat("data_local.txt").st_size == 0):
	print(f"File empty, gathering data")

	s.sendall(b'get_data\n')
	
	with open(filename, 'w') as file: #'w' overwrites file of same filename, 'a' appends
		while True:
			data = s.recv(34) #recieve 34 bits at a time, since each entry in data.txt is 34 bits long
			
			if not data or data == b'get_data\n':  # Prevent writing the command to file
				break
				
			# print(f"Writing to '{filename}'\n")
			file.write(data.decode('utf-8'))
			file.flush()  # Ensure immediate writing to the file from program buffer
		       
else:

		while True:
			most_recent()
			time.sleep(2)

