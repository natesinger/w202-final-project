#!/usr/bin/python3

import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 54321

START_INDICATOR = b'\xDE\xAD\xBE\xEF'
STOP_INDICATOR = b'\xBE\xEF\xDE\xAD'
major_options = b'\x01' #one byte
minor_options = b'\xCD\xEF' #three bytes
payload = b'A'*1012 #1012 bytes of payload space
checksum = b'\xFF' #one byte calculated by adding each byte in succession mod \xFF

def send_test_frame():
    test_frame = START_INDICATOR + major_options + minor_options + payload + checksum + STOP_INDICATOR

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.connect((SERVER_HOST,SERVER_PORT))
        io.send(test_frame)
        time.sleep(2)
        io.close()
