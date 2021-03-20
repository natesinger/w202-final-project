#!/usr/bin/python3
from space_vehicle.sv_core import *
from misc.tools import ansi_esc
import argparse

def run():
    """
    usage: space.py [-h] [-p <1234>]

    Run the <w202-final> server for SV emulation.

    optional arguments:
      -h, --help            show this help message and exit
      -p <54321>, --port <54321>
                            Bind port, ephemeral prefered, default is 54321
    """

    parser = argparse.ArgumentParser(description='Run the <w202-final> server for SV emulation.')
    parser.add_argument('-p', '--port', dest='port', type=int, metavar='<1234>',
                        help='Bind port, ephemeral prefered, default is 1234')
    args = parser.parse_args()

    #override default port if specified
    bind_port = 54321
    if args.port != None: bind_port = args.port

    #abort if port invalid range, type checked by argparse
    if not (0 < bind_port < 65535): exit("[!] Invalid port specification")

    #warn if port is non-ephemeral
    if bind_port < 49152: print(f"{ansi_esc(93)}[!]{ansi_esc(0)} Port is non-ephemeral, may need to ensure correct perms and deconflict...")

    run_sv(bind_port)

if __name__ == "__main__":
    run()
