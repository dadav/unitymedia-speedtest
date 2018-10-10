#!/bin/bash

if [[ $VIRTUAL_ENV = "" ]]; then
  echo "Use virtualenv"
  exit 1
fi

echo "Install python requirements"
pip install -r requirements.txt 2>/dev/null

echo "Create Servicefile"
cat >umtest.service <<EOF
[Unit]
Description=Unitymedia speedtest

[Service]
Type=oneshot
Environment=http_proxy=$http_proxy https_proxy=$https_proxy no_proxy=$no_proxy
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$VIRTUAL_ENV/bin/python check.py

[Install]
WantedBy=multi-user.target
EOF

echo "Create timer"
cat >umtest.timer <<EOF
[Unit]
Description=Start Unitymedia Speedtest

[Timer]
OnBootSec=15min
OnUnitActiveSec=6h

[Install]
WantedBy=timers.target
EOF

sudo cp umtest.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now umtest.timer
