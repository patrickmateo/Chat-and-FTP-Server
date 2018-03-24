import socket
import threading
import Modules.DES as DES
import Modules.shared as shared
import Modules.getfile as getfile
import Modules.sendfile as sendfile

class ClientChat2:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x = input("Please enter the IP address:\t")
    host = str(x)
    z = input("Please enter the Port Number:\t")
    port = int(z)

    print("\n\n***************************************************\n"
          "***\t To use the service please type: \t***\n"
          "***\t'ftransfer' for file transfer\t\t***\n"
          "***\t'exchangekey' for exhanging of keys\t***\n"
          "***\t'descrypt' for encrypting\t\t***\n"
          "***\t'logout' to log out to the server\t***\n"
          "***************************************************\n"
          "To send messages just press <enter> to send\n")

    def sendMSG(self):

        while True:
            x = input("")
            if x == "ftransfer":
                self.getSend()
            elif x == "exchangekey":
                shared.cls.main()
            elif x == "descrypt":
                DES.cls.openfile()
            elif x == 'logout':
                self.sock.close()
                print("goodbye!")
                exit()
            else:
                self.sock.send(bytes(x, 'ascii'))

    def getSend(self):
        choice = input("Please type rec for to recieve file or \n"
              "type send to send file to your partner: \t")
        if choice == 'rec':
            print("Closing the chat server..")
            #self.sock.close()
            getfile.cls.main()
        elif choice == 'send':
            print("Closing the chat server..")
            #self.sock.close()
            sendfile.cls.main()
        else:
            print("Invalid Input! Please try again")

    def __init__(self):

        #try:
        self.sock.connect((self.host, self.port))

        inThread = threading.Thread(target=self.sendMSG)
        inThread.daemon = True
        inThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'ascii'))
"""
        except WindowsError:
            print("Cannot connect to the server. Please try again!")
"""
client  = ClientChat2()

