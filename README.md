# Linux_Syslog_Detector

An automated Python tool for parsing Linux system logs to detect brute-force attempts and unauthorized access patterns. Designed to parse Linux authentication logs (`auth.log`) on the fly, this tool detects brute-force attempts, unauthorized privilege escalation, and high-risk root access events.

## Features

**Real-Time Monitoring:** Mimics the behavior of `tail -f` using Python file-pointer manipulation (`seek` / `readline`) for low CPU overhead.
**Threat Detection Triggers:** Automatically flags and outputs alerts for:
    - Brute-force login failures (`Failed password`)
    - Reconnaissance probes for non-existent users (`Invalid user`)
    - Unauthorized privilege escalation (`NOT in sudoers`)
    - Critical security risks (Direct root logins)

## Tech Stack

**Language:** Python3
**Environment:** Linux (Ubuntu / Raspberry Pi OS)
**Core Modules:** Built-in `time` library (zero heavy external dependencies)

## Setup & Usage

1. **Configure Environment & Firewall:**
Follow the step-by-step setup guide in [LAB_NOTES.md](./LAB_NOTES.md) to configure your Linux environment, secure SSH access via UFW, and locate your system log paths.

2. **Run the Detector:**
Because system logs require root privileges to read, execute the script with `sudo`:

   ```bash
   sudo python3 Main.py
   ```
