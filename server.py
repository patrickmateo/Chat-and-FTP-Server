import socket
import threading

class serverChat:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientConn = []
    def __init__(self):
        global prime
        global base
        host = socket.gethostbyname(socket.gethostname())
        port = 7899
        self.sock.bind((host,port))
        self.sock.listen(1)
        print("Server running on %s:%d..." %(host, port))

    def printer(self):
        print(prime)


    def connHandler(self,c,a):

        while True:
            try:
                data = c.recv(1024)
                msg = data.decode('ascii')
                dataX = bytes("<"+str(a[0])+":"+str(a[1])+">:\t"+msg, 'ascii')
                for connection in self.clientConn:
                    connection.send(dataX)
                if not data:
                    print(str(a[0]) + ':' + str(a[1]),' disconnected')
                    self.clientConn.remove(c)
                    c.close()
                    break
            except WindowsError:
                print(str(a[0]) + ':' + str(a[1]), 'disconnected')
                self.clientConn.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            clientThread = threading.Thread(target=self.connHandler, args=(c,a))
            clientThread.daemon = True
            clientThread.start()
            self.clientConn.append(c)
            print(str(a[0]) + ':' + str(a[1]) + ' is connected')

serverChat =  serverChat()
serverChat.run()