# Import socket module 
import socket             
 
# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 65432               
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
 
# receive data from the server and decoding to get the string.


#s.send('get_data\n'.encode('utf-8'))
#print (s.recv(1024).decode('utf-8'))
# close the connection
s.send('get_data_after[2025-03-09][22:47:11.63]\n'.encode('utf-8'))

try:
    while True:
        data = s.recv(1024)
        print(data.decode('utf-8'))
        if not data:
            break
        #print("Received data:", data.decode())
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    s.close()

#s.send('get_data_after[2025-03-09][22:47:11.63]\n'.encode('utf-8'))

#s.close()
