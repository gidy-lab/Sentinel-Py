#!/bin/bash
PROJECT_DIR=$(pwd)
USER_NAME=$(whoami)

echo "[*] Installing Sentinel-Py for user: $USER_NAME"

# 1. System Setup
sudo apt update && sudo apt install -y python3-venv rsyslog ssh
sudo systemctl enable rsyslog ssh
sudo systemctl start rsyslog ssh

# 2. Python Setup
python3 -m venv venv
./venv/bin/pip install flask flask-sqlalchemy

# 3. Create the Background Service (Permanent Fix)
sudo bash -c "cat <<EOF > /etc/systemd/system/sentinel-collector.service
[Unit]
Description=Sentinel-Py Collector
After=rsyslog.service

[Service]
ExecStart=${PROJECT_DIR}/venv/bin/python3 ${PROJECT_DIR}/collector.py
Restart=always
User=root
WorkingDirectory=${PROJECT_DIR}

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable sentinel-collector.service
sudo systemctl restart sentinel-collector.service

# 4. Create Desktop Shortcut
cat <<EOF > ~/Desktop/Sentinel-SIEM.desktop
[Desktop Entry]
Name=Sentinel SIEM
Exec=bash -c 'cd ${PROJECT_DIR} && ./venv/bin/python3 app.py'
Icon=security-high
Terminal=true
Type=Application
EOF

chmod +x ~/Desktop/Sentinel-SIEM.desktop
gio set ~/Desktop/Sentinel-SIEM.desktop metadata::trusted true

echo "[+] 100% COMPLETE. Double-click the icon on your desktop!"