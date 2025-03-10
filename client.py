# Import socket module 
import socket             
 
# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 65432               
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
 
# receive data from the server and decoding to get the string.


s.send('get_data\n'.encode('utf-8'))
print (s.recv(1024).decode('utf-8'))
# close the connection


s.close()
