#!/usr/bin/python3

import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 54321

START_INDICATOR = b'\xDE\xAD\xBE\xEF'
STOP_INDICATOR = b'\xBE\xEF\xDE\xAD'

## TODO need to write the port arg and overwrite

def run_communication(selection:str, options:str, payload:str):
    print(f"Selection: {selection}\nOptions: {options}\nPayload: {payload}")
    if payload == None: payload = b'\xFF' * 1012 #if no payload specified
    if len(payload) < 1012: payload = payload + (b'\xFF' * (1012 - len(payload)))

    checksum = generate_checksum(START_INDICATOR + selection + options + payload + STOP_INDICATOR)

    test_frame = START_INDICATOR + selection + options + payload + checksum + STOP_INDICATOR

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.connect((SERVER_HOST,SERVER_PORT))

        print(selection)
        print(options[0])

        if (selection == b'\x01') and (options[0] == 1): #key wipe
            io.send(test_frame)
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 2): #key select
            io.send(test_frame)
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 3): #key write
            exchange_key(io, options[1])
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x01') and (options[0] == 4): #key regenerate
            for index in range(15): exchange_key(io, index)
            time.sleep(2) #doesnt trip on itself due to threading
        elif (selection == b'\x02') and (options[0] == 2): #data exchange
            pass
        elif (selection == b'\x03') and (options[0] == 2): #firmware validation
            pass

        io.close()

def exchange_key(io:object, index:int):
    print(f'exchanging key {index}')
    io.send(b'ground 1')
    print(io.recv())
    time.sleep(2)
    io.send(b'ground 2')
    print(io.recv())
    time.sleep(2)
    io.send(b'ground 3')
    print(io.recv())


    #1 recieve public knowledge, p and g
    #1r send ack
    #2 recieve public key from ground
    #2r send public key to ground
    #3 recieve symetric key
    #3r send ack to ground


def generate_checksum(frame_data):
    #this is generated as single byte addition mod \xFF but skipping the checksum byte position obviously
    return b'\xFF'
