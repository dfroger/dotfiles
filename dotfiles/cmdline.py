#!/usr/bin/env python
import argparse
import sys

def parse_command_line(argv=None):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--source_dir', '-s',
                        help='Path to source directory')

    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose mode')

    parser.add_argument('--no-action', '-n', action='store_true',
                        help='Do not actually do anything, just log action')

    parser.add_argument('action', choices=['status', 'install'])

    if argv == None:
        argv = sys.argv
        argv.pop(0)

    args = parser.parse_args(argv)
    return args
