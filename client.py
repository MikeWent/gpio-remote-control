#!/usr/bin/env python3
import argparse
import socket

DEFAULT_SERVER_PORT = 28010
DEFAULT_SERVER_IP = "127.0.0.1"

args = argparse.ArgumentParser()
args.add_argument("-p", "--port", help="server port to bind, default is {}".format(DEFAULT_SERVER_PORT), type=int, default=DEFAULT_SERVER_PORT)
args.add_argument("-i", "--ip", help="IP address to bind, default is {}".format(DEFAULT_SERVER_IP), default=DEFAULT_SERVER_IP)
args.add_argument("-n", "--pin", help="GPIO pin number", type=int, required=True)
ex_args = args.add_mutually_exclusive_group(required=True)
ex_args.add_argument("-v", "--value", metavar="N", help="new GPIO pin value tp set", type=int, choices=(0, 1, 2))
ex_args.add_argument("-s", "--switch", help="switch pin value like toggle, alias for '--value 2'", action="store_true")
options = args.parse_args()

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server
    try:
        sock.connect((options.ip, options.port))
    except ConnectionRefusedError:
        print("Connection refused. Is server running and {} port open?".format(options.port))
        exit(1)
    # Build a command
    value = 2 if options.switch else options.value
    command = "{} {}".format(options.pin, value)
    # Send command
    sock.sendall(bytes(command, "ascii"))
    # Get response (100 bytes maximum)
    received = str(sock.recv(100), "ascii")

if "ERR" in received:
    print("Server answered with '{}'".format(received))
    exit(1)
