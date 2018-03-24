import socket
import os


class sendfile:

    def main(self):
        search = input("Please enter the name of the text file \n"
                       "or type ls to list all the filesin this directory : \t")
        if search == 'ls':
            listFiles = os.listdir()
            print("\n***List of files in this directory***\n")
            for x in listFiles:
                print(x)
            print("\n***End of files***\n")
            self.main()
        else:
            fname = search
            self.filetransfer(fname)

    def filetransfer(self,fname):
        port = 6969
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host, port))
        s.listen(5)

        print('Ready to send file.. Waiting for the reciever...')

        conn, addr = s.accept()
        print('Connected from IP:', addr)
        data = conn.recv(1024)
        print('', repr(data))
        filename = fname
        file = open(filename, 'rb')
        listfile = file.read(1024)
        while (listfile):
            conn.send(listfile)
            print('Sending.. ', repr(listfile))
            listfile = file.read(1024)
        file.close()
        print('Transferring of file done!')
        print('File transfer will now quit..')
        conn.close()

cls = sendfile()
