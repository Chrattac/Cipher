import math as m
import random


######################################
# RSA
class RSA:
    @staticmethod
    def cipher(message, e, n):
        ciphered = ""
        for letter in message:
            letter = ((ord(letter)**e)%n)
            ciphered+=chr(letter)
        
        return ciphered
        

    @staticmethod
    def decipher(message, d, n):
        deciphered = ""
        for letter in message:
            letter = ((ord(letter)**d)%n)
            deciphered+=chr(letter)
        
        return deciphered


    @staticmethod
    def get_parameters():
        done = False

        while(not done):
            try: RSA_p = int(input("Give RSA 'p' parameter: "))
            except ValueError:
                print("Please enter an integer!")
                continue
            else: 

                if(is_prime(RSA_p)):

                    while(not done):

                        try: RSA_q = int(input("Give RSA 'q' parameter: "))
                        except ValueError:
                            ValueError: print("Please enter an integer!")
                            continue
                        else:

                            if(is_prime(RSA_q)):
                                RSA_n = RSA_p*RSA_q
                                RSA_phi = (RSA_p - 1)*(RSA_q -1)

                                while(not done):

                                    try: RSA_e = int(input("Give RSA 'e' parameter: "))
                                    except ValueError:
                                        print("Please enter an integer!")
                                        continue
                                    else:

                                        if RSA_e < 1 and RSA_e > RSA_phi: print("e must be in between 1 and {0}".format(RSA_phi))
                                        elif GCD(RSA_e, RSA_phi) == 1: done = True
                                        else: print("Greatest common divisor for e and phi wasn't 1")

                            else: print("You didn't give prime!")

                else: print("You didn't give prime!")

        ##Extended euclidean for RSA_d:
            x1, y1, z1 = 1, 0, RSA_e
            x2, y2, z2 = 0, 1, RSA_phi
            while z2 != 0:
                d = z1//z2 #Divisor to use gives integer rounded down, ie: RSA_e//RSA_phi = d (+0.xxx...)
                x2, x1 = x1-d*x2, x2 #1st iteration: x2 = 1 - d * 0; x1 = 0 => 2nd: x2 = 0 - d * (1 - d * 0); y1 = 1 - d * 0...
                y2, y1 = y1-d*y2, y2 #1st iteration: y2 = 0 - d * 1; y1 = 1 => 2nd: y2 = 1 - d * (0 - d * 1); y1 = 0 - d * 1...
                z2, z1 = z1-d*z2, z2 #1st iteration: z2 = RSA_e - d * RSA_phi; z1 = RSA_phi => 2nd: z2 = RSA_phi - d * (RSA_e - d*RSA_phi); z1 = (RSA_e - d*RSA_phi)...
                # Will be continued till we get z2 == 0 (z2 start value RSA_e)
            RSA_d = x1%RSA_phi
            
        return RSA_e, RSA_n, RSA_d         

########################################################
# Caesar uses all unicode characters, base shift is 300
class Caesar:
    
    @staticmethod
    def cipher(message, offset=0):
        base = 300
        ciphered = ""
        offset += base #add base to offset

        for letter in message:
            letter=chr((ord(letter)+offset)%1114112) # 1114112 amount of unicode characters in UTF-8 table according to various sources
            ciphered+=letter

        return ciphered
    
    @staticmethod
    def decipher(message, offset):
        base = 300
        offset += base #add base to offset
        deciphered = ""

        for letter in message:
            letter=chr((ord(letter)-offset)%1114112)
            deciphered+=letter

        return deciphered

#########################
def xor_str(message, key):
    xorred_string = ""
    i=0
    for letter in message:
        letter = ord(letter) ^ ord(key[i])
        i+=1
        xorred_string += chr(letter)
        if i==len(key): i=0

    return xorred_string

#########################
def GCD(x, y):
    if y == 0: return x
    return GCD(y, x%y)

#########################
def is_prime(num):
    '''Returns true if given number is prime'''
    prime = True
    if num != 2:
        for n in (2,m.ceil(num/2)):
            if num%n == 0:
                prime = False
                break
    
    return prime

#############
###PROGRAM### :
#############



print("Welcome!")
handled_lines = []
file_name = input("Give name of the plaintext file: ")
crypt_name = input("Give name of the crypted file: ")

while(True):
    try: offset = int(input("Give the caesar shift: "))
    except ValueError: 
        print("Please give integer: ")
        continue
    else: break

xor_key = input("Give the key you want to xor with: ")

xor_key = Caesar.cipher(xor_key, offset)

print("Then for RSA")
e, n, d = RSA.get_parameters()

print("Public: ({x}, {y})".format(x=e, y=n))
print("Private: ({x}, {y})".format(x=d, y=n))

while(True):
    try: choice = int(input("Do you want to [1] cipher, [2] decipher or [9] quit: "))
    except ValueError: print("Please give int!")
    else:
        if((choice == 1) or (choice == 2) or (choice == 9)): break
        else: print("Choose either 1 or 2!")

if choice == 1:
    try: f = open(file_name, 'r')
    except FileExistsError: print("file {0} not found".format(file_name))
    else:
        lines = f.readlines()
        f.close()
        print("##### CRYPTING FILE #####")
        for line in lines:
            if line is lines[-1]:
                line = Caesar.cipher(line, offset)
                line = xor_str(line, xor_key)
                line = RSA.cipher(line, e, n)
                handled_lines.append(line)
            else:
                line = Caesar.cipher(line[:-1], offset)
                line = xor_str(line, xor_key)
                line = RSA.cipher(line, e, n)
                handled_lines.append(line+'\n')
        f = open(crypt_name, 'w+')
        f.truncate()
        f.writelines(handled_lines)
        f.close()

elif choice == 2:
    try: f = open(crypt_name, 'r')
    except FileNotFoundError: print("file {0} not found".format(crypt_name))
    else:
        lines = f.readlines()
        f.close()
        print("##### Decrypting FILE #####")
        for line in lines:
            if line is lines[-1]:
                line = RSA.decipher(line, d, n)
                line = xor_str(line, xor_key)
                line = Caesar.decipher(line, offset)
                handled_lines.append(line)
            else:
                line = RSA.decipher(line[:-1], d, n)
                line = xor_str(line, xor_key)
                line = Caesar.decipher(line, offset)
                handled_lines.append(line+'\n')
        f = open(file_name, 'w+')
        f.truncate()
        f.writelines(handled_lines)
        f.close()











