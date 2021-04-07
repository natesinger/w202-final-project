from space_vehicle.simulated_memory import *
import time

def keymgmt_select(keynumber:int):
    print(f"[!] Key selection [{keynumber+1}] requsted...")
    with SpaceMemoryManager() as m:
        m.write_keyselection(keynumber)
    time.sleep(1)
    print("[+] Key selection applied...")
