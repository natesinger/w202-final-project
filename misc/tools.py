#short random utilities go here
import time

#define ANSI escape for coloring: https://en.wikipedia.org/wiki/ANSI_escape_code
def ansi_esc(code): return f'\033[{code}m'

#make a loading bar
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
