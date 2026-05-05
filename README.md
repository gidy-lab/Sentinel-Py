# Sentinel-Py // Lightweight SIEM & SOC Dashboard

Sentinel-Py is a Python-based Security Information and Event Management (SIEM) tool designed for Linux environments. It monitors system logs in real-time to detect unauthorized access and policy violations.

## 🛡️ Core Features
- **Real-Time Log Analysis:** Monitors `/var/log/auth.log` for instant threat detection.
- **Threat Intelligence:** Integrated IP tracing via AbuseIPDB.
- **SOC Dashboard:** A dark-themed web interface for security analysts to monitor events.
- **Incident Management:** Ability to purge logs and export security reports to CSV.

## 🔐 Detection Capabilities
- **SSH Brute Force:** Detects multiple failed login attempts.
- **Privilege Escalation:** Monitors unauthorized or suspicious `sudo` command usage.
- **Policy Violations:** Tracks system changes like new user creation or password modifications.

## 🛠️ Technology Stack
- **OS:** Kali Linux (Host)
- **Language:** Python 3
- **Framework:** Flask (Backend)
- **Database:** SQLite with SQLAlchemy
- **Frontend:** HTML5, CSS3 (SOC Dark Theme)

## 🚀 How to Run
1. Clone the repository.
2. Run the collector: `python3 collector.py`
3. Start the dashboard: `python3 app.py`
4. Access the SOC at `http://127.0.0.1:5000`


