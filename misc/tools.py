#short random utilities go here
import time
import random
import math
import secrets ##best library for Generating secure random numbers for managing secrets

#define ANSI escape for coloring: https://en.wikipedia.org/wiki/ANSI_escape_code
def ansi_esc(code): return f'\033[{code}m'

#make a loading bar
def listening_activity_bar(delay:float=1.0):
    while True:
        try: #load 'da bar
            for i in range(8):
                if i == 0: print('Connection open... (XOOOO)', end = "\r")
                elif i == 1: print('Connection open... (OXOOO)', end = "\r")
                elif i == 2: print('Connection open... (OOXOO)', end = "\r")
                elif i == 3: print('Connection open... (OOOXO)', end = "\r")
                elif i == 4: print('Connection open... (OOOOX)', end = "\r")
                elif i == 5: print('Connection open... (OOOXO)', end = "\r")
                elif i == 6: print('Connection open... (OOXOO)', end = "\r")
                elif i == 7: print('Connection open... (OXOOO)', end = "\r")
                time.sleep(delay)
        except KeyboardInterrupt:
            return



########## --- Mariah Working Code -- #######
##Note secrets library only exists in python3
##Checked return value against sagemath library in cocal is_prime(# returned)

def generate_Random_Prime_Number(bit_Length: int):
    """Generates a random large prime number of provided byte size
    """
    while True:
        primeNum = secrets.randbits(bit_Length)
        if is_Prime(primeNum):
            return primeNum


## From Invent with python Exercises: https://inventwithpython.com/cracking/chapter22.html
def is_Prime(test_Number: int):
    # Return True if num is a prime number, simple, slightly faster way to check if it is a prime number than RabinMiller
    if (test_Number < 2):
        return False  # 0, 1, and negative numbers are not prime.
    for i in range(2, int(math.sqrt(100)) + 1):
        if test_Number % i == 0:
            return False
    return rabin_Miller(test_Number)


## From Invent with python Exercises: https://inventwithpython.com/cracking/chapter22.html
def rabin_Miller(test_Number: int):
    # Returns True if number provided is a prime number.
    if test_Number % 2 == 0 or test_Number < 2:
        return False  # Rabin-Miller doesn't work on even integers.
    if test_Number == 3:
        return True
    s = test_Number - 1
    t = 0
    while s % 2 == 0:
        # Keep halving s until it is odd (and use t
        # to count how many times we halve s):
        s = s // 2
        t += 1
    for trials in range(10):  # Try to falsify num's primality 5 times.
        a = random.randrange(2, test_Number - 1)
        v = pow(a, s, test_Number)
        if v != 1:  # This test does not apply if v is 1.
            i = 0
            while v != (test_Number - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % test_Number
    return True


def calculate_Private_Key(byte_length: int, p: int):
    """
    Provided a byte length, find a random exponent (integer value)
    of that bit size -1  to use as a private key for Diffie-Hellman
    (Code from cocalc examples provided by Kevin)
    """
    upper_limit = (p - 2)
    lower_limit = ((p - 2) // 2)

    private_key = int(random.randint(lower_limit, upper_limit))
    return private_key


def generate_Large_Random_Number(byte_size: int):
    """ Provided a byte size/length , find a random number of that bit size """
    number = secrets.randbits(byte_size)
    return number


def generate_Public_Key(g: int, private_key: int, prime_number: int):
    """Calculate a public key using the provided generator, private key, and large prime number
    TODO: fix issue with prime number being larger than 50 bit size
    """
    pkey = pow(g,private_key, prime_number ) # formula for creating the public key.  pow(g, private_key) % p
    return pkey


def calculate_Shared_Key(g: int, public_key_a: int, public_key_b: int, prime_number: int):  # Exchange public keys to use for calculating the shared key (Diffie-Hellman step 4-5)
    """Calculate the shared key using the provided ground public key, space public key, and large prime number"""
    ## Original attempt:
    #K = pow(public_key_a, public_key_b) % prime_number  ## Idea is :  pow(g, kakb) % prime_number

    kakb = public_key_a * public_key_b
    #print(f'kakb = {kakb}, g = {g}, p = {prime_number}')
    sharedKey = pow(g, kakb, prime_number)
    return sharedKey


def calculate_generator(prime_number: int):
    '''
    TODO: Currently implementing generator to calculate the primitive root for a large prime number
    '''
    phi = prime_number - 1
    prime_number_set = set()

    while (phi % 2 == 0):
        prime_number_set.add(2)
        phi = phi // 2

    # phi must be odd
    # skip one element (Note i = i +2)
    for i in range(3, int(math.sqrt(phi)), 2):
        while (phi % i == 0):
            prime_number_set.add(i)
            phi = phi // i
    if (phi > 2):
        prime_number_set.add(phi)

    phi = prime_number - 1
    for possible_gen in range(2, phi + 1):
        flag = False
        for val in prime_number_set:
            ## --
            resultVal = 1
            x = possible_gen % prime_number
            divisor = phi // val

            while (divisor > 0):
                if (divisor & 1):
                    resultVal = (resultVal * x) % prime_number
                divisor = divisor >> 1  # y = y/2
                x = (x * x) % prime_number
                ## --
            if (resultVal == 1):  # r^((phi)/primefactors) % n ?= 1 --> might need to implement different check here?
                flag = True
                break

        # If there was no power with value 1.
        if (flag == False):
            return possible_gen

            # Print Error? -> No primitive root found if -1 returned
    return -1


#### Main for Testing:

def main():
    p = generate_Random_Prime_Number(32)  ## Tested in pycharm and cocal for sizes up to 58 so far will succesfully find g

    g = calculate_generator(p)  ## for p = generate_Random_Prime_Number(58)  -test case - successsful - 4/2/2021 -3:18AM
                                #   if p = generate_Random_Prime_Number( numberUsed>58 )
    print(f' prime number: {p} \n generator: {g} ')

    ground_private_key = calculate_Private_Key(32,p)  # -test case - successful for p with bit size 22 - 4/2/2021 -3:18AM
    space_private_key = calculate_Private_Key(32,p)  # -test case - successful for p with bit size 22 - 4/2/2021 -3:18AM

    # ground_private_key = calculate_Private_Key(22, 1607267198020003997) # -test case - successfull - 4/2/2021 -3:20AM
    # space_private_key = calculate_Private_Key(22, 1607267198020003997)  # -test case - successful - 4/2/2021 -3:20AM

    print(f' ground private key: {ground_private_key}')
    print(f' space private key: {space_private_key}' )

    ground_public_key = generate_Public_Key(g, ground_private_key, p)  ## -- issue here -- no problem until p bit size 25 or larger
    space_public_key = generate_Public_Key(g, space_private_key, p)

    # ground_public_key = generate_Public_Key(2, ground_private_key, 1607267198020003997) ## -- issue here -- no problem until  size 25 or larger for p , but generator can be found for this value
    # space_public_key = generate_Public_Key(2, space_private_key, 1607267198020003997)

    print(f' ground public key: {ground_public_key} ')
    print(f' space public key: {space_public_key}')

    shared_key = calculate_Shared_Key(g,ground_public_key, space_public_key,p)  ## --issue at size 23 (takes long  time - need to figure out more efficient method)

    print(f' shared key: {shared_key}')


if __name__ == '__main__':
    main()
