#!/usr/bin/python3

import socket

BIND_HOST = 'localhost'
BIND_PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
    io.bind((BIND_HOST,BIND_PORT))
    io.listen()
    
    while True:
        conn, addr = io.accept()
        
        with conn:
            print('[+] New connection from {}'.format(addr))
            
            while True:
                data = conn.recv(1024) #1kb chunks
                if not data:
                    break
                print(data)

            print('[-] Connection closed from {}'.format(addr))
