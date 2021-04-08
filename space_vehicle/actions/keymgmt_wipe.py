from space_vehicle.simulated_memory import *
import time

def keymgmt_wipe():
    print("[!] Memory wipe requsted...")
    with SpaceMemoryManager() as m:
        m.clear()
    time.sleep(1)
    print("[+] Memory wipe complete...")
