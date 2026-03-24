import os
import re
import subprocess
from datetime import datetime
from app import db, Alert, app

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'siem.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

def monitor_log():
    process = subprocess.Popen(['tail', '-F', '/var/log/auth.log'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("[-] Sentinel-Py SOC is actively scanning for threats...")

    while True:
        line = process.stdout.readline()
        if not line: continue

        event_type = None
        severity = "Info"

        # 1. Detect Brute Force
        if "Failed password" in line:
            event_type = "SSH Brute Force"
            severity = "High"
        
        # 2. Detect Privilege Escalation (Sudo)
        elif "sudo:" in line and "COMMAND=" in line:
            event_type = "Privilege Escalation"
            severity = "Medium"
            
        # 3. Detect Policy Violations (User/Group changes)
        elif any(x in line for x in ["new user", "new group", "password changed"]):
            event_type = "Policy Violation"
            severity = "High"

        if event_type:
            ip_match = re.search(r'from ([\d\.]+)|from (localhost)', line)
            ip_address = "127.0.0.1"
            if ip_match:
                raw_val = ip_match.group(1) or ip_match.group(2)
                ip_address = "127.0.0.1" if raw_val == "localhost" else raw_val

            with app.app_context():
                new_alert = Alert(
                    timestamp=datetime.now(),
                    event_type=event_type,
                    source_ip=ip_address,
                    message=line.strip()[:100] + "...",
                    severity=severity
                )
                db.session.add(new_alert)
                db.session.commit()
                print(f"[!] {event_type} detected!")

if __name__ == "__main__":
    monitor_log()