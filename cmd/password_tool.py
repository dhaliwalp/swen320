# command line
import sys
from Cipher import Cipher

if __name__ == "__main__":
    #number = len(sys.argv)
    #print("Arguments count: " + str(number))
    #for i, arg in enumerate(sys.argv):
    #    print(str(i) + ":" + arg)
    if len(sys.argv) == 1:
        print(len(sys.argv))
        exit(1);
        
    cipher = Cipher()
    if sys.argv[1] == "-d":
        encPassword = sys.argv[2]
        print("decrypt...")
        plainText = cipher.decrypt(encPassword)
        print(plainText)
    
    if sys.argv[1] == "-e":
        print("encrypt...")
        plainPassword = sys.argv[2]
        encText = cipher.encrypt(plainPassword)
        print(encText)