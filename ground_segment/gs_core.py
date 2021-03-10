#!/usr/bin/python3

import socket

SERVER_HOST = 'localhost'
SERVER_PORT = 1234

start_indicator = b'\xDE\xAD\xBE\xEF'
stop_indicator = b'\xBE\xEF\xDE\xAD'
operation = b'\x01' #one byte
options = b'\xCD\xEF' #three bytes
payload = b'A'*1012 #1012 bytes of payload space
checksum = b'\xFF' #one byte calculated by adding each byte in succession mod \xFF

test_frame = start_indicator + operation + options + payload + checksum + stop_indicator

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
    io.connect((SERVER_HOST,SERVER_PORT))
    io.send(test_frame)
