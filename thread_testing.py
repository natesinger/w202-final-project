#!/usr/bin/python3
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def worker(x:int):
    for i in range(10):
        print(f"{time.time()} Thread {x}")
        time.sleep(0.5)

def my_service():
    logging.debug('Starting')
    time.sleep(3)
    logging.debug('Exiting')
1
w1 = threading.Thread(name='my_service', target=worker, args=(1,))
w2 = threading.Thread(name='my_service', target=worker, args=(2,))
w3 = threading.Thread(name='my_service', target=worker, args=(3,))

w1.start()
w2.start()
w3.start()

import time

"""def worker(x:int):
    for i in range(10):
        print(f"{time.time()} Thread {x}")
        time.sleep(0.1)
"""
