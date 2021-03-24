#!/usr/bin/python3
from ground_segment.gs_core import *
from misc.tools import ansi_esc
import argparse

def run():
    """
    usage:
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
    parser.add_argument('-k', '--key-management', dest='keymgmt', type=str, metavar='<wipe|write|select>',
                        help='Asymetric key management operations')
    parser.add_argument('-d', '--send-data', dest='senddata', type=str, metavar='<mov periapse deg 12>',
                        help='Send commands or data to SV flight computer')
    parser.add_argument('-s', '--signature-validation', dest='signature_validation', type=bool,
                        help='Request a SHA-256 hash of the SV memory space')
    args = parser.parse_args()


    ## TODO make sure we check that an option was actually selected, else help
    ## TODO fix signature validation so its just a boolean flag

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
            options = b"\x01"
        elif (args.keymgmt == 'select'):
            key_index = get_index()
            options = b"\x02" + key_index ## TODO need to validate this
        elif (args.keymgmt == 'write'):
            key_index = get_index()
            options = b"\x03" + key_index ## TODO need to validate this
        else: #valid operation, proceed
            print(f"[!] Invalid key management operation: {args.keymgmt}")
            exit()

    send_data = None
    if args.senddata != None:
        total_commands_selected += 1
        selection = b'\x02'

    if args.signature_validation != None: #this needs to get fixed
        total_commands_selected += 1
        selection = b'\x03'

    ## TODO validation to ensure two operations are not happening at once
    if total_commands_selected > 1:
        print("[!] Multiple operations selected, this is not currently supported")
        exit()

    run_communication(selection, options, payload)

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

    return int(key_index).to_bytes(1, byteorder='big')

if __name__ == "__main__":
    run()
