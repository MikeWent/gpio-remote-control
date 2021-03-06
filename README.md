# GPIO remote control

Control your Raspberry Pi GPIO remotely with TCP socket.

Requirements: Python 3.5+

## How to use

### Server

Run `server.py` on your Raspberry Pi. This can be (and should be) done with systemd.

```bash
$ git clone https://github.com/MikeWent/gpio-remote-control && cd gpio-remote-control
$ ./install-systemd-unit.sh
```

- to start server: `sudo systemctl start gpio-remote-control`
- to stop server: `sudo systemctl stop gpio-remote-control`

Server runs on `28010` port on all interfaces & all addresses (`0.0.0.0` stands for it) by default. This behavior can be changed via editing the `install-systemd-unit.sh` file (run it again after editing):

```ini
ExecStart=/usr/bin/python3 $PWD/server.py --systemd --ip 192.168.12.34 --port 1234
```

### Client

Use `client.py` as remote control (see `$ ./client.py --help`). You can alternatively use `nc` (OpenBSD netcat) to send commands (see examples below).

### Examples

Edit `client.py` to set `DEFAULT_SERVER_IP` or use `-i/--ip` flag as shown below.

```bash
# set pin 18 to 1 (HIGH)
$ ./client.py --pin 18 --value 1
# set pin 18 to 0 (LOW)
$ ./client.py --pin 18 --value 0

# switch pin 18 (see Client protocol)
$ ./client.py --pin 18 --switch

# more compact syntax
$ ./client.py -n 18 -v 1
# for switch
$ ./client.py -n 18 -s

# with IP specified
$ ./client.py --ip 192.168.1.2 -n 18 -v 1
# with port specified
$ ./client.py --port 1234 -n 18 -v 1
```

### With netcat

```
$ nc 192.168.1.2 28010
18 1<Enter>
```

### Pipes and netcat

```bash
$ echo "18 1" | nc 192.168.1.2 28010
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
   - `command OK` if everything is fine
   - `command PERM ERR` if changing the pin's value isn't permitted for some reason

## License

MIT
