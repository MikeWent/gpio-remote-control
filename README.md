# GPIO remote control

Control your Raspberry Pi GPIO remotely with TCP socket.

## How to use

Run `server.py` on your Raspberry Pi.

Then use `client.py` as remote control (see `$ ./client.py --help`). You can alternatively use `nc` (OpenBSD netcat) to send commands (see examples below).

Server runs on `28010` port on all interfaces & all addresses (`0.0.0.0` stands for it) by default. This behavior can be changed via editing `server.py` (line 7 and 8).

### Examples

Edit `client.py` to set `DEFAULT_SERVER_IP` or use `-i/--ip` flag as shown below.

```bash
# set pin 18 to 1 (HIGH)
$ ./client.py --pin 18 --value 1
# set pin 18 to 0 (LOW)
$ ./client.py --pin 18 --value 0

# more compact syntax
$ ./client.py -n 18 -v 1

# with IP specified
$ ./client.py --ip 192.168.1.2 -n 18 -v 1

# with IP and port specified
$ ./client.py -i 192.168.1.2 -p 1234 -n 18 -v 1
```

### With netcat

```
$ nc 192.168.1.2 28010
18 1<Enter>
```

### Pipes and netcat

```bash
$ echo "18 1" | nc 192.168.1.2 28010
18 1 OK
```

## Client protocol

Implemented in `client.py`, more details: `$ ./client.py --help`.

1. Connect to server via default TCP socket interface.
2. Send a command, for example `18 1`, which means "switch pin `18` to value `1`".

   See available pins on [pinout.xyz](https://pinout.xyz).

   Available values: `0` -> LOW, `1`-> HIGH, `2` -> switch (non-standard), means "switch pin's value from 1 to 0 or from 0 to 1 depending on it's current value".

3. Get response from the server (optionally).

   The response can be:
   - `SYNTAX ERR` if server cannot understand the command
   - `command PERM ERR` if changing the pin's value isn't permitted for some reason

## License

MIT
