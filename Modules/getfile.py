import socket

class getfile:

    def main(self):
        try:
            x = input("Please type the IP address you want to connect:\t")
            s = socket.socket()
            host = x
            port = 6969
            s.connect((host, port))
            s.send(bytes("Connection established with the receiver..",'ascii'))
            print("%s:%s"%(host, port))
            with open('downloaded.txt', 'wb') as f:
                print('Downloading file...')
                while True:
                    print('Receiving data...')
                    data = s.recv(1024)
                    print('data=%s', (data))
                    if not data:
                        break
                    f.write(data)
            f.close()
            print('File successfully downloaded!')
            s.close()
            print('The connection will now close..')
        except WindowsError:
            print("The connection to the send could not be found!")
cls = getfile()
