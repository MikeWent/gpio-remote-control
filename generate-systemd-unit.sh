#!/bin/bash

# info
name="gpio-remote-control"
desc="Control Raspberry Pi GPIO remotely"
documentation="https://github.com/MikeWent/gpio-remote-control"

# generate
echo "[Unit]
Description=$desc
Documentation=$documentation

[Service]
Type=simple
ExecStart=/usr/bin/python3 $PWD/server.py
Restart=always
RestartSec=5
User=$USER
WorkingDirectory=$PWD

[Install]
WantedBy=multi-user.target" > $name.service

# apply
sudo mv $name.service /lib/systemd/system/
sudo systemctl daemon-reload && echo "Service: $name.service"
