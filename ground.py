#!/usr/bin/python3
from ground_segment.gs_core import send_test_frame
from misc.tools import ansi_esc
import argparse

def run():
    """
    usage:
    """
    parser = argparse.ArgumentParser(description='Run the <w202-final> client for connection to SV.')
    #parser.add_argument(dest='<address> <>', metavar='<file>', type=str, nargs='+',
    #                    help='file(s) to operate on, typical argument vector \"**argv\"')
    parser.add_argument('-a', '--address', dest='address', type=str, metavar='<152.132.18.19>',
                        help='Server address, default is \'localhost\'')
    parser.add_argument('-p', '--port', dest='port', type=int, metavar='<54321>',
                        help='Server port, ephemeral prefered, default is 54321')
    parser.add_argument('-st', '--static-test', dest='test', action='store_true',
                        help='Static test frame')
    args = parser.parse_args()

    #override default ip
    server_address = '127.0.0.1'
    if server_address != None: server_address = args.address

    #override default port
    server_port = 54321
    if args.port != None: server_port = args.port

    #warn if port is non-ephemeral
    if server_port < 49152: print(f"{ansi_esc(93)}[!]{ansi_esc(0)} Port is non-ephemeral, may need to ensure correct perms and deconflict...")

    send_test_frame()

"""
    #Prevent file overwrite
    if os.path.isfile(args.out_file): input("[!] Output file {} already exists, press [Enter] to continue with append...".format(args.out_file))

    #Execute on specified files, if a dir or bad perms, etc, then fail gracefully
    savedata = []
    for file in args.files:
        try: savedata.append(parse_ais_file(file,radius_mi,float(coordinate[0]),float(coordinate[1])))
        except: print("[!] Couldnt process {}".format(files))

    for file_result in savedata:
        with open(args.out_file, 'a') as fh: #append
            for entry in file_result:
                fh.write("{}\n".format(entry['data']))

    print("Found {} entries within {} miles of {}, {}".format(sum(1 for line in open(args.out_file)),radius_mi,coordinate[0],coordinate[1]))
"""
if __name__ == "__main__":
    run()
