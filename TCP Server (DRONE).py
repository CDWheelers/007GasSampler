import socket
import time

def send(data, port):
    s = socket.socket()
    s.bind(('', port))
    s.listen(5)
    c, addr = s.accept()
    print ('Got connection from',addr)
    c.send(str(data).encode())
    c.close()

if __name__ == '__main__':
    port = 1025
    num = 1
while True:
            print ('hey, sending data')
            words = 'helloWorld'
            data = words + str(num)
            print ('send data: %s' % data)
            send(data,port)
            port = port + 1
            num = num + 1
