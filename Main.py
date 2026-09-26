import time

log_path = "/var/log/auth.log"

print(f"[*] Starting detector... watching {log_path}")

with open(log_path, "r") as f:
    f.seek(0,2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        
        if "Failed password" in line:
            print(f"[ALERT!] Login failure detected: {line.strip()}")
            
        elif "Invalid user" in line:
            print(f"[ALERT!] Probe for non-existent user: {line.strip()}")
            
        elif "NOT in sudoers" in line:
            print(f"[ALERT!] Unauthroized sudo usage: {line.strip()}")
            
        elif "Accepted publickey for root" in line or "Accepted password for root" in line:
            print(f"[ALERT!] Direct root login detected: {line.strip()}")
        