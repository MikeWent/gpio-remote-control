#!/bin/bash

name="gpio-remote-control"

sudo systemctl stop "$name.service" 2> /dev/null # hide output if service doesn't exist

echo "[Unit]
Description=Raspberry Pi GPIO remote control
Documentation=https://github.com/MikeWent/gpio-remote-control
Wants=network-online.target
After=network.target network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $PWD/server.py --systemd --ip 0.0.0.0 --port 28010
Restart=always
RestartSec=5
User=$USER
WorkingDirectory=$PWD

[Install]
WantedBy=multi-user.target" > $name.service

sudo mv $name.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable "$name.service"
sudo systemctl start "$name.service"
echo "Service '$name.service' started and enabled on startup"
