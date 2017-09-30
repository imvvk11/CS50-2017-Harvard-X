
import sys

def caesar():
    result = ""
    if len(sys.argv) == 2:
        key = int(sys.argv[1]) % 26
        word = input("Plaintext: ")
        length = len(word)
        for i in word:
            if i.isalpha():
                num = ord(i)
                num += key
                if i.isupper():
                    if num > ord('Z'):
                        num -= 26

                    elif num < ord('A'):
                        num += 26

                elif i.islower():
                    if num > ord('z'):
                        num -= 26

                    elif num < ord('a'):

                        num += 26

                result += chr(num)

        print ("Ciphertext: {0}".format(result))


    else:
        print ("python caesar.py key")
caesar()
