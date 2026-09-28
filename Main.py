import re
import subprocess
import time
from collections import defaultdict

log_path = "/var/log/auth.log"  

failed_attempts = defaultdict(list)

# Configuration thresholds
MAX_FAILURES = 5 
TIME_WINDOW = 60  
BLOCK_IPS = False 


def extract_ip(line: str):
    """
    Extracts an IPv4 address from a log line using Regex.
    
    Args:
        line (str) : Alert that's triggered in the log
    """
    match = re.search(r"(?:from|rhost=)([0-9]{1,3}(?:\.[0-9]{1,3}){3})", line)
    return match.group(1) if match else None


def block_ip(ip_address):
    """
    Executes an iptables command to block an IP address.
    
    Args: 
        ip_address (str) : Attacker's IP address generated in the alert
    """
    if not BLOCK_IPS:
        print(f"[SIMULATION] Would block IP: {ip_address}")
        return

    try:
        # Command to drop all incoming traffic from this IP
        cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
        result = subprocess.run(cmd, captureButton=True, text=True, check=True)
        print(f"[CRITICAL BLOCK!] Successfully blocked IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to block IP {ip_address}: {e.stderr}")


print(f"[*] Starting advanced detector... watching {log_path}")

try:
    with open(log_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            current_time = time.time()
            ip = extract_ip(line)

            # --- Failed Password / Brute-Force Tracking ---
            if "Failed password" in line:
                print(f"[ALERT!] Login failure: {line.strip()}")
                if ip:
                    failed_attempts[ip] = [
                        t
                        for t in failed_attempts[ip]
                        if current_time - t < TIME_WINDOW
                    ]
                failed_attempts[ip].append(current_time)

                # Check if threshold
                if len(failed_attempts[ip]) >= MAX_FAILURES:
                    print(
                        f"[THRESHOLD BREACH] IP {ip} hit {len(failed_attempts[ip])}"
                        " failures in "
                        f"{TIME_WINDOW}s."
                    )
                    block_ip(ip)
                    # Clear tracking for this IP
                    failed_attempts[ip] = []

            # --- RULE 2: Invalid Users---
            elif "Invalid user" in line:
                print(f"[ALERT!] Probe for non-existent user: {line.strip()}")
                if ip:
                    pass

            # --- RULE 3: Unauthorized Sudo ---
            elif "NOT in sudoers" in line:
                print(f"[ALERT!] Unauthorized sudo usage: {line.strip()}")

            # --- RULE 4: Root Logins ---
            elif (
                "Accepted publickey for root" in line
                or "Accepted password for root" in line
            ):
                print(
                    f"[CRITICAL SECURITY ALERT!] Direct root login detected:"
                    f" {line.strip()}"
                )

except FileNotFoundError:
    print(
        f"[ERROR] Log file not found at {log_path}. Are you running on Linux with"
        " root permissions?"
    )
except KeyboardInterrupt:
    print("\n[*] Detector stopped by user. Exiting safely.")