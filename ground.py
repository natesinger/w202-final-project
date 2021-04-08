#!/usr/bin/python3
from ground_segment.gs_core import *
from ground_segment.actions.assemble_payload import *
from misc.tools import ansi_esc
import argparse
import math
import base64
from Crypto import Random
from ground_segment.simulated_memory import *
import time
import pyaes
import base64

def run():
    """
    usage: ground.py [-h] [-a <152.132.18.19>] [-p <54321>] [-k <wipe|regenerate|write|select>]
                 [-d <mov periapse deg 12>] [-s]

    Run the <w202-final> client for connection to SV.

    optional arguments:
      -h, --help            show this help message and exit
      -a <152.132.18.19>, --address <152.132.18.19>
                            Server address, default is 'localhost'
      -p <54321>, --port <54321>
                            Server port, ephemeral prefered, default is 54321
      -k <wipe|regenerate|write|select>, --key-management <wipe|regenerate|write|select>
                            Asymetric key management operations
      -d <mov periapse deg 12>, --send-data <mov periapse deg 12>
                            Send commands or data to SV flight computer
      -s, --signature-validation
                            Request a SHA-256 hash of the SV memory space
    """
    selection = None
    options = None
    payload = None
    total_commands_selected = 0

    parser = argparse.ArgumentParser(description='Run the <w202-final> client for connection to SV.')
    #parser.add_argument(dest='<address> <>', metavar='<file>', type=str, nargs='+',
    #                    help='file(s) to operate on, typical argument vector \"**argv\"')
    parser.add_argument('-a', '--address', dest='address', type=str, metavar='<152.132.18.19>',
                        help='Server address, default is \'localhost\'')
    parser.add_argument('-p', '--port', dest='port', type=int, metavar='<54321>',
                        help='Server port, ephemeral prefered, default is 54321')
    parser.add_argument('-k', '--key-management', dest='keymgmt', type=str, metavar='<wipe|regenerate|write|select>',
                        help='Asymetric key management operations')
    parser.add_argument('-d', '--send-data', dest='senddata', type=str, metavar='<mov periapse deg 12>',
                        help='Send commands or data to SV flight computer')
    parser.add_argument('-s', '--signature-validation', dest='signature_validation', action='store_true',
                        help='Request a SHA-256 hash of the SV memory space')
    args = parser.parse_args()

    #override default ip
    server_address = '127.0.0.1'
    if server_address != None: server_address = args.address

    #override default port
    server_port = 54321
    if args.port != None: server_port = args.port

    #warn if port is non-ephemeral
    if server_port < 49152: print(f"{ansi_esc(93)}[!]{ansi_esc(0)} Port is non-ephemeral, may need to ensure correct perms and deconflict...")

    #validate key management input if relevant
    key_index = None
    if args.keymgmt != None:
        total_commands_selected += 1
        selection = b'\x01'

        if (args.keymgmt == 'wipe'):
            options = b"\x01\xFF"
        elif (args.keymgmt == 'select'):
            key_index = get_index()
            options = b"\x02" + key_index ## TODO need to validate this
        elif (args.keymgmt == 'write'):
            key_index = get_index()
            options = b"\x03" + key_index ## TODO need to validate this
        elif (args.keymgmt == 'regenerate'):
            options = b"\x04\xFF" ## TODO need to validate this
        else: #valid operation, proceed
            print(f"[!] Invalid key management operation: {args.keymgmt}")
            exit()

        p = (541).to_bytes(32, byteorder='big') #256 bit, but have to do this because it doesnt work rn
        g = (101010).to_bytes(8, byteorder='big')
        #g = calculate_generator(p) #this doesnt work

        payload = p + g

    send_data = None
    if args.senddata != None:
        if len(args.senddata) > 992:
            print("[!] Currently cannot handle payloads over 992 bytes")
            exit()

        total_commands_selected += 1
        selection = b'\x02'

        key = None
        with GroundMemoryManager() as m:
            key = m.read_key()

        aes = pyaes.AESModeOfOperationCTR(key)
        plaintext = args.senddata
        ciphertext = aes.encrypt(plaintext)
        payload = base64.b64encode(ciphertext)

        print(f"[!] Sending CT (b64 encoded): {payload.decode()}")
        options = len(payload).to_bytes(2, byteorder='big')

    if args.signature_validation != False: #this needs to get fixed
        total_commands_selected += 1
        selection = b'\x03'
        options = b'\xFF\xFF'

    ## TODO validation to ensure two operations are not happing at once
    if total_commands_selected > 1:
        print("[!] Multiple operations selected, this is not currently supported")
        exit()
    elif total_commands_selected < 1: #no options selected
        parser.print_help()
        exit()
    else:
        #print(f"Selection: {selection}\nOptions: {options}\nPayload: {payload}")
        #set initial payload for key exchange here due to runing out of time
        run_communication(selection, options, payload) #execute

def get_index():
    key_index = input("Please provide a key index [1-15]: ")
    badkey = False
    try:
        if not (1 <= int(key_index) <= 15): badkey = True #specification outside keyspace
    except: #probably provided a string, likely type conversion failed
        badkey = True
    finally:
        if not badkey:
            print(f"Valid key selection {key_index}")
        else:
            print(f"Invalid key index {key_index}")
            exit()

    return (int(key_index)-1).to_bytes(1, byteorder='big')

if __name__ == "__main__":
    run()
