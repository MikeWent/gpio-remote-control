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
    # Connect to server and send data
    sock.connect((options.ip, options.port))
    if options.switch:
        value = 2
    else:
        value = options.value
    command = "{} {}".format(options.pin, value)
    sock.sendall(bytes(command, "ascii"))
    received = str(sock.recv(100), "ascii")

if "ERR" in received:
    print("Server answered with '{}'".format(received))
    exit(1)

if "OK" in received:
    exit(0)
