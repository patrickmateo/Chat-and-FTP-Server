import os
import binascii

pc1 = [56, 48, 40, 32, 24, 16, 8,
       0, 57, 49, 41, 33, 27, 17,
       9, 1, 58, 50, 42, 34, 26,
       18, 10, 2, 59, 51, 43, 35,
       62, 54, 46, 38, 30, 22, 14,
       6, 61, 53, 45, 37, 29, 21,
       13, 5, 60, 52, 44, 36, 28,
       20, 12, 4, 27, 19, 11, 3]

pc2 = [13, 16, 10, 23, 0, 4,
       2, 27, 14, 5, 20, 9,
       22, 18, 11, 3, 25, 7,
       15, 6, 26, 19, 12, 1,
       40, 51, 30, 36, 46, 54,
       29, 39, 50, 44, 32, 47,
       43, 48, 38, 55, 33, 52,
       45, 41, 49, 35, 28, 31]

dictSBox = {}
dictSBox[0] = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], \
              [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], \
              [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], \
              [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], \
              [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], \
              [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], \
              [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], \
              [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7]

dictSBox[1] = [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], \
              [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], \
              [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], \
              [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], \
              [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], \
              [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], \
              [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], \
              [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2]

dictSBox[2] = [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], \
              [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], \
              [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], \
              [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], \
              [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], \
              [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], \
              [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], \
              [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8]

dictSBox[3] = [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13], \
              [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9], \
              [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12], \
              [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14], \
              [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3], \
              [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13], \
              [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12], \
              [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]

ip = [57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7,
      56, 48, 40, 32, 24, 16, 8, 0,
      58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, ]

ebit = [31, 0, 1, 2, 3, 4,
        3, 4, 5, 6, 7, 8,
        7, 8, 9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31, 0]

iterationShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

finalPermute = [15, 6, 19, 20,
                28, 11, 27, 16,
                0, 14, 22, 25,
                4, 17, 30, 9,
                1, 7, 23, 13,
                31, 26, 2, 8,
                18, 12, 29, 5,
                21, 10, 3, 24]

inverseIP = [39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25,
             32, 0, 40, 8, 48, 16, 56, 24]
msgDict = []
storeMSG = []

class DES:

    prime = 23


    def openfile(self):
        try:
            search = input("Please enter the name of the text file \n"
                       "or type ls to list all the filesin this directory : \t")
            if search == 'ls':
                listFiles = os.listdir()
                print("\n***List of files in this directory***\n")
                for x in listFiles:
                    print(x)
                print("\n***End of files***\n")
                self.openfile()
            else:
                fname = search

                keyShare = input("Please enter the shared key given by your partner: \t")
                ownKey = input("Please enter your own key: \t")
                ultisecretKey = (int(keyShare) ** int(ownKey)) % self.prime
                print("The secret key is : \t%d" %(ultisecretKey))
                self.chooser(ultisecretKey,fname)
        except:
            print("Invalid input, please try again")

    def chooser(self, ultisecretKey, fname):
        choice = input("Please type enc for encrypt or dec for decrypt : \t")
        if choice == 'enc':
            key = str(ultisecretKey)
            path = str(fname)
            self.encrypt(key,path)
        elif choice == 'dec':
            key = str(ultisecretKey)
            path = str(fname)
            self.decrypt(key, path)
        elif choice == 'exit':
            exit()
        else:
            print("Invalid input please try again")


    def encrypt(self,key,path):
        print("Getting ready to encrypt!")
        print(key)
        print(path)
        cls.startEncrypt(key,path)
        del msgDict[:]
        del storeMSG[:]
        return

    def decrypt(self,key,path):
        print("Getting ready to decrypt!")
        print(key)
        print(path)
        cls.startDecrypt(key,path)
        del msgDict[:]
        del storeMSG[:]
        return

    def startEncrypt(self,key,fname):
        print(key)
        cls.computeFileEnc(key,fname)
        return

    def computeFileEnc(self,key,fname):
        try:
            ftxt = open(fname,'rb')
            text = ftxt.read()
            print('Text Content: %s'%(text))
            samp = binascii.hexlify(text)
            ftxt.close()
            ftxt2 = open(fname, 'wb')
            ftxt2.write(samp)
            ftxt2.close()

            for i in range(0, len(samp), 16):
                x = (samp[i: i + 16])
                x = (str(x))
                x = x[2:((len(x) - 1))]
                msgDict.append(x)
            print('Number of times will encrypt: %s'%(len(msgDict)))
            origMessage = text
            origKey = key

            for i in range(len(msgDict)):
                print('\n********** Encryption Round %s **********' % (i + 1))
                b = msgDict[i]
                x = cls.keyConvertEnc(key)
                y = cls.messageConvertEnc(b)
                cls.permuteInitialEnc(x,y,origKey,origMessage)
            cls.fileSaveEnc(fname)
        except ValueError:
            print('Error! Please input hexadecimal only in textfile!')
        return

    def fileSaveEnc(self,fname):
        fileOriginal = ''.join(msgDict)
        fileNew = ''.join(storeMSG)
        ftxt = open(fname, 'w')
        ftxt.write(fileNew)
        ftxt.close()
        print('\nText Input: \t\t%s' % (fileOriginal))
        print('Text Encrypted: \t%s' % (fileNew))
        print('File successfully updated!')
        return

    def keyConvertEnc(self,key):
        print('\nOriginal Key: \t\t%s' % (key))
        print('Round(s) chosen: \t%d' % (round))
        binKey = bin(int(key, 16))
        lKey = list(binKey[2:].zfill(64))
        keyOriginal = ''.join(lKey)
        printKey = " ".join(keyOriginal[i: i + 8] for i in range(0, len(keyOriginal), 8))
        print("Key converted to Binary (64-bit): \t\t%s" % (printKey))

        permute1 = [lKey[i] for i in pc1]
        permuteKey = ''.join(permute1)
        printKeyP = " ".join(permuteKey[i: i + 7] for i in range(0, len(permuteKey), 7))
        print("Permutation Choice 1 of Key (56-Bit):  ", printKeyP)

        pleftOrig = permuteKey[:int((len(permuteKey) / 2))]
        printPLeft = " ".join(pleftOrig[i: i + 7] for i in range(0, len(pleftOrig), 7))
        pRightOrig = permuteKey[int((len(permuteKey) / 2)):len(permuteKey)]
        printPRight = " ".join(pRightOrig[i: i + 7] for i in range(0, len(pRightOrig), 7))
        print('Left Side (28-Bit): \t \t %s' % (printPLeft))
        print('Right Side (28-Bit): \t \t %s' % (printPRight))

        lefty = permute1[:int((len(permuteKey) / 2))]
        righty = permute1[int((len(permuteKey) / 2)):len(permuteKey)]
        print('Original left side: \t \t \t' + ''.join(lefty))
        print('Original right side: \t \t \t' + ''.join(righty))

        counterRound = 0
        iteration = 0
        dictKeys = {}
        for i in iterationShift[:(round)]:
            iteration = iteration + i
            iterLeft = (lefty[iteration:] + lefty[:iteration])
            iterRight = (righty[iteration:] + righty[:iteration])
            counterRound = counterRound + 1
            iterLeftP2 = ''.join(iterLeft)
            iterRightP2 = ''.join(iterRight)
            combineLR = iterLeftP2 + iterRightP2
            print('\nRound %d : Left Side Shift %d: \t\t\t\t%s' % (counterRound, i, iterLeftP2))
            print('Round %d : Right Side Shift %d: \t\t\t\t%s' % (counterRound, i, iterRightP2))
            permute2 = [combineLR[i] for i in pc2]
            permuteKey2 = ''.join(permute2)
            dictKeys[counterRound] = [permute2]
            printKeyP2 = " ".join(permuteKey2[i: i + 4] for i in range(0, len(permuteKey2), 4))
            print("Round %d : Encrypted Binary Key (48-Bit): \t%s" % (counterRound, printKeyP2))
            keyEnc = hex(int(permuteKey2, 2))
            print('Round %d : Converted Encrypted Key: \t\t%s' % (counterRound, keyEnc[2:]))
        return dictKeys

    def messageConvertEnc(self,message):
        print('\nOriginal Message: \t\t%s' % (message))
        binMessage = bin(int(message, 16))
        lMessage = list(binMessage[2:].zfill(64))
        messageOriginal = ''.join(lMessage)
        printMessage = " ".join(messageOriginal[i: i + 4] for i in range(0, len(messageOriginal), 4))
        print("Message converted to Binary (64-bit):\t\t\t%s "%(printMessage))

        permuteIP = [lMessage[i] for i in ip]
        permuteMessageIP = ''.join(permuteIP)
        printMessageIP = " ".join(permuteMessageIP[i: i + 4] for i in range(0, len(permuteMessageIP), 4))
        print("Initial Permutation of Message (64-Bit): \t\t%s"%(printMessageIP))

        leftMOrig = permuteMessageIP[:int((len(permuteMessageIP) / 2))]
        rightMOrig = permuteMessageIP[int((len(permuteMessageIP) / 2)):len(permuteMessageIP)]
        printLeftM = " ".join(leftMOrig[i: i + 4] for i in range(0, len(leftMOrig), 4))
        printRightM = " ".join(rightMOrig[i: i + 4] for i in range(0, len(rightMOrig), 4))
        print('Message Left Side (32-Bit): \t \t %s' % (printLeftM))
        print('Message Right Side (32-Bit): \t \t %s' % (printRightM))

        dictMessage = {}
        dictMessage[0]= [leftMOrig,rightMOrig]
        return dictMessage

    def permuteInitialEnc(self,keyData,messageData,key,message):
        counterM = 0
        for i in range(1,round+1):
            print('\n********** Round %s **********'%(i))
            joinKey = ''.join(keyData[i][0])

            printKeyP2 = " ".join(joinKey[i: i + 6] for i in range(0, len(joinKey), 6))
            print("Key %d (48-Bit):  \t\t%s" % (counterM, printKeyP2))
            print('Left Message Swap with Right (32-Bit): \t\t %s' % (messageData[0][1]))

            rightMPerm = [messageData[counterM][1][i] for i in ebit]
            permuteRightM = ''.join(rightMPerm)
            printEbitRight = " ".join(permuteRightM[i: i + 6] for i in range(0, len(permuteRightM), 6))
            print("E-bit Permutation (48-Bit): \t ", printEbitRight)

            rightkeyXOR = []
            counterPermute = 0
            for i in rightMPerm:
                computed = int(i) ^ int(joinKey[counterPermute])
                rightkeyXOR.append(str(computed))
                counterPermute = counterPermute + 1

            printrkXOR = ''.join(rightkeyXOR)
            printRK = " ".join(printrkXOR[i: i + 6] for i in range(0, len(printrkXOR), 6))
            print('Right Message XOR with encrypted key: \t%s ' % (printRK))

            counter1 = 0
            counter2 = 5
            sboxStore = []
            for i in range(0, 8):
                x = printrkXOR[counter1] + printrkXOR[counter2]
                storage3 = int(x, 2)
                print("\nBinary of first and last bits (%d): \t %s" % (i + 1, storage3))
                print("Middle bits: \t%s" % (printrkXOR[(counter1 + 1):counter2]))
                print("Middle bits converted: \t%s" % (int(printrkXOR[(counter1 + 1):counter2], 2)))
                counter3 = dictSBox[storage3][i][(int(printrkXOR[(counter1 + 1):counter2], 2))]
                print("S-Box Representation: \t%s" % (counter3))
                storage2 = bin(int(counter3))
                print("S-Box Binary: \t%s" % (storage2[2:].zfill(4)))
                sboxStore.append(storage2[2:].zfill(4))
                counter2 = counter2 + 6
                counter1 = counter1 + 6

            printSBox = ''.join(sboxStore)
            printMSbox = " ".join(printSBox[i: i + 4] for i in range(0, len(printSBox), 4))
            print("\nS-Box Conversion: \t\t%s" % (printMSbox))

            permuteF = [printSBox[i] for i in finalPermute]
            pF = ''.join(permuteF)
            printPF = " ".join(pF[i: i + 4] for i in range(0, len(pF), 4))
            print("F Value: \t\t\t\t%s" % (printPF))

            rightkeyXOR2 = []
            counterPermuteF = 0
            for i in permuteF:
                computed = int(i) ^ int(messageData[counterM][0][counterPermuteF])
                rightkeyXOR2.append(str(computed))
                counterPermuteF = counterPermuteF + 1

            printrkXOR2 = ''.join(rightkeyXOR2)
            printLKFinal = " ".join(messageData[counterM][1][i: i + 4] for i in range(0, len(messageData[counterM][1]), 4))
            printRKFinal = " ".join(printrkXOR2[i: i + 4] for i in range(0, len(printrkXOR2), 4))
            print('Left Message Final: \t%s ' % (printLKFinal))
            print('Right Message Final: \t%s ' % (printRKFinal))

            x = messageData[counterM][1]
            y = printrkXOR2
            counterM = counterM + 1
            messageData[counterM] = [x,y]

        print('\nOriginal Key: \t\t\t\t\t%s' % (key))
        print('Original Message: \t\t\t\t%s' % (message))

        final = ''.join(messageData[round][1]+messageData[round][0])
        IPreverse = [final[i] for i in inverseIP]
        final2 = ''.join(IPreverse)
        printMsg = " ".join(final2[i: i + 8] for i in range(0, len(final2), 8))
        print('Encrypted Binary Message: \t\t%s'%(printMsg))
        hd = (len(final2) + 3) // 4
        hexa = '%.*x' % (hd, int('0b' + final2, 0))
        print('Converted Encrypted Message: \t%s' % (hexa))
        storeMSG.append(hexa)
        return

    def startDecrypt(self,key,fname):
        print(key)
        cls.computeFileDec(key,fname)
        return


    def computeFileDec(self,key,fname):
        try:
            ftxt = open(fname, 'r')
            text = ftxt.read()
            print('Text Content: %s' % (text))
            for i in range(0, len(text), 16):
                x = (text[i: i + 16])
                msgDict.append(x)
            print('Number of times will decrypt: %s' % (len(msgDict)))

            OrigMessage = text
            origKey = key

            for i in range(len(msgDict)):
                print('\n********** Decryption Round %s **********' % (i + 1))
                b = msgDict[i]
                x = cls.keyConvertDec(key)
                y = cls.messageConvertDec(b)
                cls.permuteInitialDec(x, y, origKey, OrigMessage)
            cls.fileSaveDec(fname)
        except ValueError:
            print('Error! Please input hexadecimal only in textfile!')
        return

    def fileSaveDec(self,fname):
        fileOriginal = ''.join(msgDict)
        fileNew = ''.join(storeMSG)
        asc1 = ''.join(chr(int(fileNew[i:i + 2], 16)) for i in range(0, len(fileNew), 2))
        ftxt = open(fname, 'w')
        ftxt.write(asc1)
        ftxt.close()
        print('\nCiphered Text: \t\t%s' % (fileOriginal))
        print('Text Decrypted: \t%s' % (asc1))
        print('File successfully updated!')
        return

    def keyConvertDec(self,key):
        print('Original Key: \t\t%s' % (key))
        print('Round(s) chosen: \t%d' % (round))
        binKey = bin(int(key, 16))
        lKey = list(binKey[2:].zfill(64))
        keyOriginal = ''.join(lKey)
        printKey = " ".join(keyOriginal[i: i + 8] for i in range(0, len(keyOriginal), 8))
        print("Key converted to Binary (64-bit): \t\t%s" % (printKey))

        permute1 = [lKey[i] for i in pc1]
        permuteKey = ''.join(permute1)
        printKeyP = " ".join(permuteKey[i: i + 7] for i in range(0, len(permuteKey), 7))
        print("Permutation Choice 1 of Key (56-Bit):  ", printKeyP)

        pleftOrig = permuteKey[:int((len(permuteKey) / 2))]
        printPLeft = " ".join(pleftOrig[i: i + 7] for i in range(0, len(pleftOrig), 7))
        pRightOrig = permuteKey[int((len(permuteKey) / 2)):len(permuteKey)]
        printPRight = " ".join(pRightOrig[i: i + 7] for i in range(0, len(pRightOrig), 7))
        print('Left Side (28-Bit): \t \t %s' % (printPLeft))
        print('Right Side (28-Bit): \t \t %s' % (printPRight))

        lefty = permute1[:int((len(permuteKey) / 2))]
        righty = permute1[int((len(permuteKey) / 2)):len(permuteKey)]
        print('Original left side: \t \t \t' + ''.join(lefty))
        print('Original right side: \t \t \t' + ''.join(righty))

        counterRound = 0
        iteration = 0
        dictKeys = {}
        for i in iterationShift[:(round)]:
            iteration = iteration + i
            iterLeft = (lefty[iteration:] + lefty[:iteration])
            iterRight = (righty[iteration:] + righty[:iteration])
            counterRound = counterRound + 1
            iterLeftP2 = ''.join(iterLeft)
            iterRightP2 = ''.join(iterRight)
            combineLR = iterLeftP2 + iterRightP2
            print('\nRound %d : Right Side Shift %d: \t\t\t\t%s' % (counterRound, i, iterLeftP2))
            print('Round %d : Left Side Shift %d: \t\t\t\t%s' % (counterRound, i, iterRightP2))
            permute2 = [combineLR[i] for i in pc2]
            permuteKey2 = ''.join(permute2)
            dictKeys[counterRound] = [permute2]
            printKeyP2 = " ".join(permuteKey2[i: i + 4] for i in range(0, len(permuteKey2), 4))
            print("Round %d : Encrypted Binary Key (48-Bit): \t%s" % (counterRound, printKeyP2))
            keyEnc = hex(int(permuteKey2, 2))
            print('Round %d : Converted Encrypted Key: \t\t%s' % (counterRound, keyEnc[2:]))
        return dictKeys

    def messageConvertDec(self,message):
        print('\nOriginal Message: \t\t%s' % (message))
        binMessage = bin(int(message, 16))
        lMessage = list(binMessage[2:].zfill(64))
        messageOriginal = ''.join(lMessage)
        printMessage = " ".join(messageOriginal[i: i + 4] for i in range(0, len(messageOriginal), 4))
        print("Message converted to Binary (64-bit):\t\t\t%s " % (printMessage))

        permuteIP = [lMessage[i] for i in ip]
        permuteMessageIP = ''.join(permuteIP)
        printMessageIP = " ".join(permuteMessageIP[i: i + 4] for i in range(0, len(permuteMessageIP), 4))
        print("Initial Permutation of Message (64-Bit): \t\t%s" % (printMessageIP))

        leftMOrig = permuteMessageIP[:int((len(permuteMessageIP) / 2))]
        rightMOrig = permuteMessageIP[int((len(permuteMessageIP) / 2)):len(permuteMessageIP)]
        printLeftM = " ".join(leftMOrig[i: i + 4] for i in range(0, len(leftMOrig), 4))
        printRightM = " ".join(rightMOrig[i: i + 4] for i in range(0, len(rightMOrig), 4))
        print('Message Left Side (32-Bit): \t \t %s' % (printLeftM))
        print('Message Right Side (32-Bit): \t \t %s' % (printRightM))
        dictMessage = {}
        dictMessage[0] = [leftMOrig, rightMOrig]
        return dictMessage

    def permuteInitialDec(self,keyData,messageData,key,message):
        counterM = 0
        counterK = round
        for i in range(1, counterK + 1):
            print('\n********** Round %s **********' % (counterK))
            joinKey = ''.join(keyData[counterK][0])

            printKeyP2 = " ".join(joinKey[i: i + 6] for i in range(0, len(joinKey), 6))
            print("Key %d (48-Bit):  \t\t%s" % (counterM, printKeyP2))
            print('Left Message Swap with Right (32-Bit): \t\t %s' % (messageData[0][1]))

            rightMPerm = [messageData[counterM][1][i] for i in ebit]
            permuteRightM = ''.join(rightMPerm)
            printEbitRight = " ".join(permuteRightM[i: i + 6] for i in range(0, len(permuteRightM), 6))
            print("E-bit Permutation (48-Bit): \t ", printEbitRight)

            rightkeyXOR = []
            counterPermute = 0
            for i in rightMPerm:
                computed = int(i) ^ int(joinKey[counterPermute])
                rightkeyXOR.append(str(computed))
                counterPermute = counterPermute + 1

            printrkXOR = ''.join(rightkeyXOR)
            printRK = " ".join(printrkXOR[i: i + 6] for i in range(0, len(printrkXOR), 6))
            print('Right Message XOR with encrypted key: \t%s ' % (printRK))

            counter1 = 0
            counter2 = 5
            sboxStore = []
            for i in range(0, 8):
                x = printrkXOR[counter1] + printrkXOR[counter2]
                storage3 = int(x, 2)
                print("\nBinary of first and last bits (%d): \t %s" % (i + 1, storage3))
                print("Middle bits: \t%s" % (printrkXOR[(counter1 + 1):counter2]))
                print("Middle bits converted: \t%s" % (int(printrkXOR[(counter1 + 1):counter2], 2)))
                counter3 = dictSBox[storage3][i][(int(printrkXOR[(counter1 + 1):counter2], 2))]
                print("S-Box Representation: \t%s" % (counter3))
                storage2 = bin(int(counter3))
                print("S-Box Binary: \t%s" % (storage2[2:].zfill(4)))
                sboxStore.append(storage2[2:].zfill(4))
                counter2 = counter2 + 6
                counter1 = counter1 + 6

            printSBox = ''.join(sboxStore)
            printMSbox = " ".join(printSBox[i: i + 4] for i in range(0, len(printSBox), 4))
            print("\nS-Box Conversion: \t\t%s" % (printMSbox))

            permuteF = [printSBox[i] for i in finalPermute]
            pF = ''.join(permuteF)
            printPF = " ".join(pF[i: i + 4] for i in range(0, len(pF), 4))
            print("F Value: \t\t\t\t%s" % (printPF))

            rightkeyXOR2 = []
            counterPermuteF = 0
            for i in permuteF:
                computed = int(i) ^ int(messageData[counterM][0][counterPermuteF])
                rightkeyXOR2.append(str(computed))
                counterPermuteF = counterPermuteF + 1
            printrkXOR2 = ''.join(rightkeyXOR2)
            printLKFinal = " ".join(
                messageData[counterM][1][i: i + 4] for i in range(0, len(messageData[counterM][1]), 4))
            printRKFinal = " ".join(printrkXOR2[i: i + 4] for i in range(0, len(printrkXOR2), 4))
            print('Left Message Final: \t%s ' % (printLKFinal))
            print('Right Message Final: \t%s ' % (printRKFinal))
            x = messageData[counterM][1]
            y = printrkXOR2
            counterM = counterM + 1
            messageData[counterM] = [x, y]
            counterK = counterK - 1

        print('\nOriginal Key: \t\t\t\t\t%s' % (key))
        print('Encrypt Message: \t\t\t\t%s' % (message))

        final = ''.join(messageData[round][1] + messageData[round][0])
        IPreverse = [final[i] for i in inverseIP]
        final2 = ''.join(IPreverse)
        printMsg = " ".join(final2[i: i + 4] for i in range(0, len(final2), 4))
        print('Decrypted Binary Message: \t\t%s' % (printMsg))
        hd = (len(final2) + 3) // 4
        hexa = '%.*x' % (hd, int('0b' + final2, 0))
        print('Decrypted Message: \t\t\t\t%s' % (hexa))
        storeMSG.append(hexa)
        print(storeMSG)
        return

cls = DES()
round = 16





