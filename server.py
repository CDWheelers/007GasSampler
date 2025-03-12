from socketserver import ThreadingTCPServer,StreamRequestHandler
from datetime import datetime

#(1) create a request handler class by subclassing the BaseRequestHandler class and overriding its handle() method
#handle() method processes incoming requests
class handler(StreamRequestHandler):
    def handle(self):
        print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
        while True:
            # get message
            msg = self.rfile.readline()
            if (msg == 'get_data\n'.encode('utf-8')):
                print(f'Received get_data cmd')
                f = open('data.txt','r')
                data = f.read()
                f.close()
                self.wfile.write(data.encode('utf-8'))
                self.wfile.flush()

            # Assume msg command is formatted as get_data_after[yyyy-mm-dd][hh:mm:ss.ms]
            if 'get_data_after'.encode('utf-8') in msg:
                print(f'Received get_data_after cmd')
                date = msg[15:25].decode('utf-8')
                time = msg[27:38].decode('utf-8')
                dateobj_a = datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M:%S.%f')
                f = open('data.txt','r')
                
                while True:
                    line = f.readline()
                    if not line:
                        break
                    print(line)
                    date = line[0:10]
                    time = line[11:22]
                    dateobj_b = datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M:%S.%f')
                    if (dateobj_b >= dateobj_a):
                        self.wfile.write(line.encode('utf-8'))

                f.close()
                self.wfile.flush()

                
            if not msg:
                print(f'Disconnected: {self.client_address[0]}:{self.client_address[1]}')
                break # exits handler, framework closes socket
            print(f'Received: {msg}')
            self.wfile.write(msg)
            self.wfile.flush()

#(2) instantiate one of the server classes, passing it the server’s address and the request handler class
#recommended to use the server in a with statement. Then call the handle_request() or serve_forever() method
#of the server object to process one or many requests. Finally, call server_close() to close the socket
#(unless you used a with statement).
server = ThreadingTCPServer(('',65432),handler)
server.serve_forever()
