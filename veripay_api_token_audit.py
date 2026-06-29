#!/usr/bin/env python3
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress insecure request warnings for testing
warnings.simplefilter('ignore', InsecureRequestWarning)

def print_banner():
    print("="*60)
    print("  Veripay API & Token Security Auditor")
    print("  Target: veripay.ng / veripaysuite.com")
    print("  Scope: Headers, Cookie Flags, Session Fixation")
    print("="*60)

def audit_security_headers(url):
    print(f"\n[*] Auditing Security Headers for: {url}")
    try:
        response = requests.get(url, verify=False, timeout=10)
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "HSTS prevents downgrade attacks",
            "Content-Security-Policy": "CSP prevents XSS",
            "X-Frame-Options": "Prevents Clickjacking",
            "X-Content-Type-Options": "Prevents MIME-sniffing"
        }
        
        missing = []
        for header, description in security_headers.items():
            if header not in headers:
                missing.append(header)
                print(f"[-] MISSING: {header} ({description})")
            else:
                print(f"[+] FOUND: {header} = {headers[header][:50]}...")
                
        if len(missing) == len(security_headers):
            print("[!] CRITICAL: Target is missing all standard security headers.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection Error: {e}")

def audit_session_cookies(url):
    print(f"\n[*] Auditing Session & Cookie Security for: {url}")
    try:
        # We perform a POST request to trigger a session cookie generation if it doesn't happen on GET
        data = {"Loginlogin": "test", "Loginpassword": "test", "LoginButton_DoLogin": "Login"}
        response = requests.post(url, data=data, verify=False, timeout=10)
        
        cookies = response.cookies
        if not cookies:
            print("[-] No cookies issued by this endpoint during failed login.")
            return

        for cookie in cookies:
            print(f"[*] Analyzing Cookie: {cookie.name}")
            flags = []
            if cookie.secure: flags.append("Secure")
            if cookie.has_nonstandard_attr('HttpOnly'): flags.append("HttpOnly")
            samesite = cookie.get_nonstandard_attr('SameSite')
            if samesite: flags.append(f"SameSite={samesite}")
            
            print(f"    Flags detected: {', '.join(flags) if flags else 'NONE'}")
            
            if not cookie.secure:
                print("    [!] VULNERABLE: Cookie sent without 'Secure' flag (can be intercepted over HTTP).")
            if not cookie.has_nonstandard_attr('HttpOnly'):
                print("    [!] VULNERABLE: Cookie sent without 'HttpOnly' flag (accessible via XSS).")
            if not samesite:
                print("    [!] VULNERABLE: Cookie missing 'SameSite' attribute (CSRF risk).")
                
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection Error: {e}")

def test_session_fixation(url):
    print(f"\n[*] Testing Session Fixation on: {url}")
    # Provide a known fake PHPSESSID
    fake_session_id = "fixation_test_12345abcdef"
    cookies = {"PHPSESSID": fake_session_id}
    data = {"Loginlogin": "invalid_user_test", "Loginpassword": "invalid", "LoginButton_DoLogin": "Login"}
    
    try:
        response = requests.post(url, cookies=cookies, data=data, verify=False, timeout=10)
        
        # Check if the server issued a NEW cookie, or accepted ours
        new_cookies = response.cookies.get_dict()
        
        if "PHPSESSID" in new_cookies and new_cookies["PHPSESSID"] != fake_session_id:
            print("[+] SECURE: Server rotated the session ID upon request/login attempt.")
        else:
            print("[!] VULNERABLE: Server accepted the provided fake PHPSESSID without rotation.")
            print("    Impact: An attacker can set a victim's session ID and hijack their account post-login.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection Error: {e}")

if __name__ == "__main__":
    print_banner()
    
    # Target 1: Modern SPA Frontend
    spa_target = "https://veripay.ng/"
    audit_security_headers(spa_target)
    
    # Target 2: Legacy State Portal (Auth Endpoint)
    legacy_auth_target = "https://www.veripaysuite.com/crs/MainLogin.php?ccsForm=Login"
    audit_session_cookies(legacy_auth_target)
    test_session_fixation(legacy_auth_target)
    
    print("\n" + "="*60)
    print("  Audit Complete.")
    print("="*60)
