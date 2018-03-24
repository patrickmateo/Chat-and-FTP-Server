
class shared:

    prime = 23
    base = 11

    def main(self):
        x = input("Please enter the client key number: \t")
        y = input("Please enter the your key number: \t")
        print("\nPublicly Shared Keys:")
        print("Your Client Key: ", x)
        print("Your Own Key:  ", y)
        print("\nComputing.... \n")
        cls.computeKey(x,y)

    def computeKey(self, x, y):
        yourpKey = (self.base ** int(y)) % self.prime
        print("Your Shared Key:\t%d" %(yourpKey) )

cls = shared()
