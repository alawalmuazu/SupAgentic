#!/usr/bin/env python3
"""
Veripay FCM API Key Verifier
Description: Tests the validity of the hardcoded Google FCM/GCM API Key found in the Android APK.
Target Key: AIzaSyBcxo2DLZsTDe_uUHfKXWJfc_mEGjLNpkI
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FCM_URL = 'https://fcm.googleapis.com/fcm/send'
# The key extracted from assets/www/sender.php inside Veripaysuite_1.3.0_APKPure.apk
API_KEY = 'AIzaSyBcxo2DLZsTDe_uUHfKXWJfc_mEGjLNpkI'

def verify_fcm_key():
    print("="*60)
    print("  Veripay FCM API Key Verification")
    print(f"  Target Key: {API_KEY[:10]}...{API_KEY[-5:]}")
    print("="*60)

    headers = {
        'Authorization': f'key={API_KEY}',
        'Content-Type': 'application/json'
    }

    # We use 'dry_run': True to test the authentication without actually sending a message
    # We use a dummy registration_id to satisfy the API payload requirements.
    payload = {
        "registration_ids": ["dummy_token_to_test_auth"],
        "dry_run": True,
        "data": {
            "message": "Security Audit Test",
            "title": "Veripay Assessment"
        }
    }

    try:
        print("[*] Sending dry-run request to FCM endpoint...")
        response = requests.post(FCM_URL, headers=headers, json=payload, verify=False, timeout=10)
        
        print(f"[-] HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[!] CRITICAL: The hardcoded API Key is VALID and ACTIVE.")
            print("[!] An attacker could use this key to blast unauthorized push notifications to all Veripay users.")
            try:
                data = response.json()
                print(f"[!] Response details: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                pass
        elif response.status_code == 401:
            print("[+] SECURE: The API Key is INVALID or has been REVOKED.")
        else:
            print(f"[-] Unexpected response. The key might be restricted by IP or Domain.")
            print(f"[-] Details: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Network Error: {e}")

if __name__ == "__main__":
    verify_fcm_key()
