#!/bin/bash

name="gpio-remote-control"

# generate
echo "[Unit]
Description=Raspberry Pi GPIO remote control
Documentation=https://github.com/MikeWent/gpio-remote-control
Wants=network-online.target
After=network.target network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $PWD/server.py --systemd
Restart=always
RestartSec=5
User=$USER
WorkingDirectory=$PWD

[Install]
WantedBy=multi-user.target" > $name.service

# apply
sudo mv $name.service /lib/systemd/system/
sudo systemctl daemon-reload && echo "Service: $name.service"
