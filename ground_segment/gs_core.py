#!/usr/bin/python3
from ground_segment.actions.keymgmt_select import *
from ground_segment.actions.keymgmt_wipe import *
from ground_segment.actions.keymgmt_write import *
from ground_segment.actions.keymgmt_regenerate import *
from ground_segment.actions.signature_validation import *
from Crypto.Util import number
import socket
import secrets
import time
import random
import hashlib
import ssl
from ground_segment.simulated_memory import *
random_function = ssl.RAND_bytes

SERVER_HOST = 'localhost'
SERVER_PORT = 54321

CLIENT_HOST = 'localhost'
CLIENT_PORT = 54322

SERVER_HOST_SECONDARY = 'localhost'
SERVER_PORT_SECONDARY = 54323

START_INDICATOR = b'\xDE\xAD\xBE\xEF'
STOP_INDICATOR = b'\xBE\xEF\xDE\xAD'

#PRIME_32 = number.getPrime(256)
PRIME_32 = 97986164599350289895243135865017426483915340502510353307949542629286511269997
GENERATOR = 2

#https://chrisvoncsefalvay.com/2016/04/27/diffie-hellman-in-under-25-lines/
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

def run_communication(selection:str, options:str, payload:str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.connect((SERVER_HOST,SERVER_PORT))

        if (selection == b'\x01') and (options[0] == 1): #key wipe
            if payload == None: payload = b'\xFF' * 1012 #if no payload specified
            if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))
            checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)
            c2_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

            keymgmt_wipe()
            io.send(c2_frame)
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 2): #key select
            if payload == None: payload = b'\xFF' * 1012 #if no payload specified
            if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))
            checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)
            c2_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

            keymgmt_select(options[1])
            io.send(c2_frame)
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 3): #key write
            if payload == None: payload = b'\xFF' * 1012 #if no payload specified
            if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))
            checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)
            c2_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

            io.send(c2_frame)
            exchange_key(options[1])
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 4): #key regenerate
            print('[!] Operation not currently supported')

            """for index in range(15):
                options = b'\x03'+(index).to_bytes(1, byteorder='big')
                run_communication(b'\x01',options,b'')
            time.sleep(2) #doesnt trip on itself due to threading"""
        elif (selection == b'\x02'): #data exchange


            if payload == None: payload = b'\xFF' * 1012 #if no payload specified
            if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))
            checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)
            c2_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

            io.send(c2_frame)
        elif (selection == b'\x03') and (options[0] == 2): #firmware validation
            pass

        io.close()

def run_communication_local(selection:str, options:str, payload:str):
    if payload == None: payload = b'\xFF' * 1012 #if no payload specified
    if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))

    checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)

    c2_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.connect((SERVER_HOST_SECONDARY,SERVER_PORT_SECONDARY))
        io.send(c2_frame)
        io.close()

def generate_checksum(frame_data):
    #this is generated as single byte addition mod \xFF but skipping the checksum byte position obviously
    return b'\xFF'

def exchange_key(index:int):
    dh_ground = DiffieHellmanKeyExchange()

    #1. sends public knowledge p and g in the first step, this is done in initial payload
    print(f'[+] Sent P/G public information')

    #THIS IS SIMPLY PASSED OVER|| NOT ACTUAL VALUES SENT
    p = PRIME_32 #256 bit, but have to do this because it doesnt work rn
    g = GENERATOR

    payload = p.to_bytes(32,byteorder='big') + g.to_bytes(8,byteorder='big')

    #1. recieves acknowledgment
    frame_chunk = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_io:
        client_io.bind((CLIENT_HOST,CLIENT_PORT))
        client_io.listen()

        conn, addr = client_io.accept()
        with conn: #conn extends contextlib
            frame_chunk = conn.recv(1024) #1kb chunks

    if frame_chunk[7:10] == b'ack': print('[+] Server acknowledged exchange(P/G)')

    time.sleep(1)

    #2. send computed public key to SV
    selection = b'\x01'
    options = b'\x03'+index.to_bytes(1,byteorder='little')

    dh_ground.generate_private_key(256)
    dh_ground.generate_public_key()
    ground_public_key_transmission = dh_ground.public_key.to_bytes(32,byteorder='big')

    run_communication_local(selection,options,ground_public_key_transmission)

    print(f'[+] Sent GS public key to SV')

    #2r Recieved public key from space
    frame_chunk = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_io:
        client_io.bind((CLIENT_HOST,CLIENT_PORT))
        client_io.listen()

        conn, addr = client_io.accept()
        with conn: #conn extends contextlib
            frame_chunk = conn.recv(1024) #1kb chunks

    sv_public_key = int.from_bytes(frame_chunk[7:39], byteorder='big')

    #calculate secret
    dh_ground.generate_secret(sv_public_key)
    print(f"[+] Got SV pubkey from vehicle downlink")
    time.sleep(1)

    #3 Calculate and send actual symmetric key for overwite
    symmetric_key = 1234567890
    symmetric_key_transmission = symmetric_key.to_bytes(32,byteorder='big')

    run_communication_local(selection,options,symmetric_key_transmission)

    print(f'[+] Sent final symmetric key (ciphertext) to vehicle for overwrite')

    #3. recieves acknowledgment
    frame_chunk = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_io:
        client_io.bind((CLIENT_HOST,CLIENT_PORT))
        client_io.listen()

        conn, addr = client_io.accept()
        with conn: #conn extends contextlib
            frame_chunk = conn.recv(1024) #1kb chunks

    if frame_chunk[7:10] == b'ack': print('[+] Server acknowledged exchange(key)')

    with GroundMemoryManager() as m:
        m.write_keyselection(index)
        m.write_key(str.encode(dh_ground.key[:32]))

    print(f'STORED KEY: {dh_ground.key[:32]}')
