from space_vehicle.frame_parser import Frame
from misc.custom_exceptions import *
import os
import threading
import socket
import time

def run_sv(bind_port:int=54321):
    """Primary function to initialize server backend, giving the user pretext and
    further coordinating thread interactions, specifically handling escape chars

    param::int::bind_port  TCP port to bind to, by default TCP/54321
    return::None **however exit within KeyboardInterrupt should be noted"""
    while True:
        try: #run the server
            input(f"Press [enter] to start the server on TCP/{bind_port}\n")

            #start server
            print(f"[+] Server started, pid:{os.getpid()}  ")
            start_server(bind_port)

            #stop server
            print(" Server stopped...                \n")

        except KeyboardInterrupt: #exit gracefully
            print() #line feed for formframe_errating
            exit()

def start_server(bind_port:int=54321):
    """Starts a new server instance and binds a socket to localhost with the
    specified port. Using localhost as opposed to the 127* so DNS may inform

    param::int::bind_port TCP port to bind to, by default TCP/54321
    return::None"""

    while True: #loop allows for server to be stopped and restarted
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as io:
                io.bind(('localhost',bind_port))
                io.listen()

                conn, addr = io.accept()
                with conn: #conn extends contextlib
                    print(f'[+] New Connection {addr}')
                    connection_bar_handle = ActiveConnectionBar()

                    while True: #hold the connection open for frame io
                        frame_chunk = conn.recv(1024) #1kb chunks
                        if not frame_chunk:
                            connection_bar_handle.kill()
                            time.sleep(2) #allow threads to die gracefully
                            break

                        try:
                            Frame(frame_chunk) #instantiate frame to process
                        except InvalidFrameError: #if parsing fails this is raised
                            print("[!] Recieved an invalid frame, the programmer probably doesnt know what he's doing")

                    print(f'[-] Connection Terminated {addr}')
        except KeyboardInterrupt: break #break on escape code
        io.close()

class ActiveConnectionBar:
    """Runs a parallel thread to display realtime indicator of active connection,
    simply executed via CR overwrite. Need to be concious of implementation, and
    stdout cleanliness... typically we can just appened whitespace

    extends::None
    class_global::kill_signal::bool allows user to request graceful exit
    class_global::delay::float specification of animation speed, smaller is faster

    None::__init__      threadbuilder for the activity bar, concurrent
    None::kill          set kill_signal high to request graceful exit
    None::__run_bar__   execute the animation, threading intended
    """

    def __init__(self, delay:float=0.2):
        self.kill_signal = False
        self.delay = delay

        worker = threading.Thread(name='connection_bar_active', target=self.__run_bar__)
        worker.start()

    def kill(self):
        self.kill_signal = True

    def __run_bar__(self):
        while not self.kill_signal:
            for i in range(4):
                if i == 0: print(f'Open connection (-)', end = "\r")
                elif i == 1: print(f'Open connection (\)', end = "\r")
                elif i == 2: print(f'Open connection (|)', end = "\r")
                elif i == 3: print(f'Open connection (/)', end = "\r")
                time.sleep(self.delay)
