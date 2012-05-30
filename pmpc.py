#!/usr/bin/env python3
#
import getopt, os, sys
import json
import socket

def usage():
    print("usage: {0} [-h host] [-p port] command".format(sys.argv[0]))
    print("commands:")
    print("\tplay wavedesc")
    sys.exit(2)

def format_command(argv):
    return json.dumps(argv)

def main():
    host = 'localhost'
    port = 6601
    opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ['help'])
    for opt, val in opts:
        if opt == '-h':
            host = val
        elif opt == '-p':
            port = int(val)
        elif opt == '--help':
            usage()
        else:
            print("unknown option:", opt, file=sys.stderr)
            usage()

    cmd = format_command(args)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(bytes(cmd, 'utf-8'))
    return 0

if __name__ == "__main__":
    sys.exit(main())
