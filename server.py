import socket             
import os
import glob

def get_latest_file(directory, extension="txt"):
    """
    Find the most recently created or modified file with the given extension.
    
    Args:
        directory (str): The directory to search in.
        extension (str): The file extension to look for.
    
    Returns:
        str: The name of the newest file, or None if no matching files exist.
    """
    files = glob.glob(os.path.join(directory, f"*.{extension}"))  # Get all .txt files
    if not files:
        return None  # No files found
    latest_file = max(files, key=os.path.getmtime)  # Get most recently modified file
    return latest_file

# next create a socket object 
s = socket.socket()         
print ("Socket successfully created")
 
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 65432               
 
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have input an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
 
# put the socket into listening mode 
s.listen(5)     
print ("socket is listening")            
 
# a forever loop until we interrupt it or 
# an error occurs 
while True:
  # Establish connection with client
  c, addr = s.accept()
  print('Got connection from', addr)

  # Get the latest .txt file
  latest_file = get_latest_file(".", "txt")

  if latest_file:
    print(f"Opening latest file: {latest_file}")
    try:
      with open(latest_file, "r") as f:
        data = f.read()
        c.send(data.encode())  # Send the contents to the client
    except Exception as e:
      print(f"Error reading file: {e}")
      c.send(f"Error reading file: {e}".encode())
  else:
    print("No .txt files found.")
    c.send("No data available.".encode())


  # Close the connection with the client 
  c.close()
   
  # Breaking once connection closed
  break
