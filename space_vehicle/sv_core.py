#!/usr/bin/python3
#from misc.tools import listening_activity_bar
import os
import threading
import socket
import time

def run_sv(bind_port:int):
    """core run"""
    while True:
        try: #run the server
            input("Press [enter] to start the server\n")

            #start server
            print(f"[+] Server started, pid:{os.getpid()}  ")
            start_server(bind_port

            #stop server
            print(" Server stopped...                \n")

        except KeyboardInterrupt: #exit gracefully
            print() #line feed for formating
            exit()

def start_server(bind_port:int):

    ## TODO: THIS NEEDS TO BE DONE AS START SERVER, GET CONNECTION, START connection open icon, then when connection drops, kill open icon
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
        io.bind(('localhost',bind_port))
        io.listen()

        conn, addr = io.accept()

        with conn:
            print(f'[+] Connection {addr}')

            #start connection bar here
            while True: #hold the connection open while the client sends data
                frame = conn.recv(1024) #1kb chunks
                if not frame: break

                print(frame)
            #stop connection here

        io.close()

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



"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
    io.bind(('localhost',bind_port))
    io.listen()

    conn, addr = io.accept()

    with conn:
        print('[+] New connection from {}'.format(addr))

        while True:
            data = conn.recv(1024) #1kb chunks
            if not data:
                break
            print(data)

        print('[-] Connection closed from {}'.format(addr))

    #x = threading.Thread(target=accept_connection(io.accept()))
    #x.start()"""
