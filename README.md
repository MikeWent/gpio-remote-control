# GPIO remote control

Control your Raspberry Pi GPIO remotely with TCP socket.

## Intro

SSH is secure but too slow to control a couple of LEDs connected to GPIO pins, so I decided to write a simple server with [socketserver](https://docs.python.org/3.5/library/socketserver.html) built-in Python library to implement **really fast** remote GPIO control.

## How to use

Run `server.py`, then use `client.py` as remote control (see `$ ./client.py --help`).

## Technical details

Server runs on `28010` port by default on all interfaces & all addresses (`0.0.0.0` stands for it). This behavior can be changed via editing `server.py` (line 7 and 8).

## Client protocol

Implemented in `client.py`, more details: `$ ./client.py --help`.

1. Connect to server via default TCP socket interface.
2. Send a `command`, for example `18 1`, which means "switch pin `18` to value `1`".

   See available pins on [pinout.xyz](https://pinout.xyz).

   Available values: `0` -> LOW, `1`-> HIGH, `2` -> switch (non-standard), means "switch pin's value from 1 to 0 or from 0 to 1 depending on it's current value".

3. Get a response from the server (optionally).

   The response can be:
   - "SYNTAX ERR" if server cannot understand the `command`
   - "`command` PERM ERR" if changing the pin's value isn't permitted for some reason

## Compatibility

You can use `nc` (OpenBSD netcat) to send commands.

Example:

```
$ nc 192.168.1.2 28010
18 1<Enter>
18 1 OK
```

Pipes and netcat:

```bash
$ echo "18 1" | nc 192.168.1.2 28010
18 1 OK
```

## License

MIT
