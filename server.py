#!/usr/bin/env python3
import argparse
import logging
import socketserver
from os.path import exists as path_exists
from time import sleep

args = argparse.ArgumentParser()
args.add_argument("-p", "--port", help="TCP port to bind, default is 28010", type=int, default=28010)
args.add_argument("-i", "--ip", help="IP address to bind, default is 0.0.0.0", type=str, default="0.0.0.0")
args.add_argument("--systemd", help="indicate that server was started by systemd (don't use when starting by hands)", action="store_true")
options = args.parse_args()

def gpio_set(pin, value):
    """Set GPIO pin to value"""
    if not path_exists("/sys/class/gpio/gpio{}".format(pin)):
        # Export pin
        with open("/sys/class/gpio/export", "w") as f:
            f.write(str(pin))
        sleep(0.05)
        # Set pin direction to "out"
        with open("/sys/class/gpio/gpio{}/direction".format(pin), "w") as f:
            f.write("out")
        sleep(0.05)
    # Set value
    with open("/sys/class/gpio/gpio{}/value".format(pin), "w") as f:
        f.write(str(value))

def gpio_switch(pin):
    """If GPIO pin is set to 1, then set it to 0 and vice versa"""
    # If pin isn't even imported, then import and set to 0
    if not path_exists("/sys/class/gpio/gpio{}".format(pin)):
        gpio_set(pin, 0)
        return
    with open("/sys/class/gpio/gpio{}/value".format(pin)) as f:
        current_pin_value = int(f.read())
    if current_pin_value != 1:
        gpio_set(pin, 1)
    elif current_pin_value != 0:
        gpio_set(pin, 0)
    else:
        gpio_set(pin, 1)

class TCPHandler(socketserver.BaseRequestHandler):
    """This class handles all incoming TCP connections"""
    def handle(self):
        # Decode bytes (default TCP stream) to ASCII text
        command = str(self.request.recv(4), "ascii")
        client_ip = self.client_address[0]
        logging.debug("recv '%s' from %s", command, client_ip)
        # Try to parse command string
        try:
            pin, value = command.split(" ")
            # Check if pin & value types are valid
            assert 0 < int(pin) < 100
            assert int(value) in (0, 1, 2)
        except:
            # Command is invalid
            logging.warn("invalid command '%s' (from %s)", command, client_ip)
            response = bytes("SYNTAX ERR", "ascii")
            self.request.sendall(response)
            return
        # Command is valid, process it
        try:
            if value == "2":
                logging.info("switch pin #%s (from %s)", pin, client_ip)
                gpio_switch(pin)
            else:
                logging.info("set pin #%s to %s (from %s)", pin, value, client_ip)
                gpio_set(pin, value)
            response = bytes(command+" OK", "ascii")
            self.request.sendall(response)
        except PermissionError:
            if value == "2":
                logging.warn("permission error: switch pin #%s", pin)
            else:
                logging.warn("permission error: set pin #%s to %s", pin, value)
            response = bytes(command+" PERM ERR", "ascii")
            self.request.sendall(response)

if __name__ == "__main__":
    if options.systemd:
        log_message_format = "%(levelname)s: %(message)s"
    else:
        log_message_format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_message_format, datefmt="%m-%d %H:%M:%S")
    logging.info("starting server on %s:%s", options.ip, options.port)
    try:
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer((options.ip, options.port), TCPHandler)
        logging.debug("server started on %s:%s", *server.server_address)
        server.serve_forever()
    except KeyboardInterrupt:
        print() # add newline after ^C in terminal
        logging.critical("interrupted by user")
        server.shutdown()
        exit()
    except OSError as e:
        logging.debug("OSError %s", e)
        logging.critical("Address/port is already in use. Is another instance of server running?")
