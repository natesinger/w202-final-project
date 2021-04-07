import socket
import time
import random
import hashlib
import ssl
random_function = ssl.RAND_bytes

START_INDICATOR = b'\xDE\xAD\xBE\xEF'
STOP_INDICATOR = b'\xBE\xEF\xDE\xAD'

CLIENT_HOST = 'localhost'
CLIENT_PORT = 54322

SERVER_HOST_SECONDARY = 'localhost'
SERVER_PORT_SECONDARY = 54323

PRIME_32 = None
GENERATOR = 2

class DiffieHellmanKeyExchange:
    def __init__(self, key_length=256):
        self.key_length = max(256, key_length)
        self.prime = PRIME_32
        self.generator = GENERATOR
    def generate_private_key(self, length):
       _rand = 0
       _bytes = length // 8 + 8
       while(_rand.bit_length() < length):
           _rand = int.from_bytes(random_function(_bytes), byteorder='big')
       self.private_key = _rand
    def generate_public_key(self):
        self.public_key = pow(self.generator, self.private_key, self.prime)
    def generate_secret(self, public_key):
        self.shared_secret = pow(public_key, self.private_key, self.prime)
        shared_secret_bytes = self.shared_secret.to_bytes(self.shared_secret.bit_length() // 8 + 1, byteorder='big')
        hash_alg = hashlib.sha256()
        hash_alg.update(bytes(shared_secret_bytes))
        self.key = hash_alg.hexdigest()

def run_communication_local(selection:str, options:str, payload:str):
    if payload == None: payload = b'\xFF' * 1012 #if no payload specified
    if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))

    checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)

    test_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.connect((CLIENT_HOST,CLIENT_PORT))
        io.send(test_frame)
        io.close()

def generate_checksum(frame_data):
    #this is generated as single byte addition mod \xFF but skipping the checksum byte position obviously
    return b'\xFF'

def calculate_Private_Key(bit_length: int, p: int):
    """
    Provided a byte length, find a random exponent (integer value)
    of that bit size -1  to use as a private key for Diffie-Hellman
    (Code from cocalc examples provided by Kevin)
    """
    upper_limit = (p - 2)
    lower_limit = ((p - 2) // 2)

    private_key = int(random.randint(lower_limit, upper_limit))
    return private_key

def generate_Public_Key(g: int, private_key: int, prime_number: int):
    """Calculate a public key using the provided generator, private key, and large prime number
    TODO: fix issue with prime number being larger than 50 bit size
    """
    pkey = pow(g,private_key, prime_number ) # formula for creating the public key.  pow(g, private_key) % p
    return pkey

def keymgmt_write(index:int, payload:str):
    print(f"[!] Recieved key-overwrite request, index: {index}")

    #1. recieves public knowledge p and g
    PRIME_32 = int.from_bytes(payload[:32], byteorder='big')
    dh_sv = DiffieHellmanKeyExchange()
    #g = int.from_bytes(payload[32:40], byteorder='little')

    print(f"  [+] Recieved pre-computed public information from ground")

    time.sleep(1)

    #1r. sends acknowledgment
    options = b'\x03'+index.to_bytes(1,byteorder='little')
    run_communication_local(b'\x01',options,b'ack')
    print(f"  [+] Sent acknowledgment")

    #2. recieve computed pubkey from ground
    frame_chunk = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_io:
        server_io.bind((SERVER_HOST_SECONDARY,SERVER_PORT_SECONDARY))
        server_io.listen()

        conn, addr = server_io.accept()
        with conn: #conn extends contextlib
            frame_chunk = conn.recv(1024) #1kb chunks

    ground_public_key = int.from_bytes(frame_chunk[7:39], byteorder='big')
    print(f"  [+] Got pubkey from ground segment")
    time.sleep(1)

    #2r. sends SV public key to ground
    selection = b'\x01'
    options = b'\x03'+index.to_bytes(1,byteorder='little')

    dh_sv.generate_private_key(256)
    dh_sv.generate_public_key()
    sv_public_key_transmission = dh_ground.public_key.to_bytes(32,byteorder='big')

    run_communication_local(selection,options,sv_public_key_transmission)
    print(f"  [+] Sent SV public key down to ground")

    #3. recieve computed symmetric key from ground and store
    frame_chunk = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_io:
        server_io.bind((SERVER_HOST_SECONDARY,SERVER_PORT_SECONDARY))
        server_io.listen()

        conn, addr = server_io.accept()
        with conn: #conn extends contextlib
            frame_chunk = conn.recv(1024) #1kb chunks

    #calculate secret
    dh_sv.generate_secret(int.from_bytes(frame_chunk[7:39], byteorder='big'))
    print(f"  [+] Got symmetric key from ground segment")
    time.sleep(1)

    #3r. sends acknowledgment
    options = b'\x03'+index.to_bytes(1,byteorder='little')
    run_communication_local(b'\x01',options,b'ack')
    print(f"  [+] Sent acknowledgment")

    print(f'GS P: {PRIME_32}')
    print(f'GS G: {GENERATOR}')
    print(f'GS PUBLIC: {dh_sv.public_key}')
    print(f'GS PRIVATE: {dh_sv.private_key}')
    print(f'GS FINAL KEY: {dh_sv.key}')
