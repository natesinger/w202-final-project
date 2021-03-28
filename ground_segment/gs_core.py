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
        io.send(test_frame)
        time.sleep(2) #doesnt trip on itself due to threading
        io.close()

def generate_checksum(frame_data):
    #this is generated as single byte addition mod \xFF but skipping the checksum byte position obviously
    return b'\xFF'
