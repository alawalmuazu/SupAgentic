import time
import sys
import random

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def simulated_loading_bar(task, duration, width=40):
    sys.stdout.write(f"{Colors.CYAN}[*] {task}...{Colors.ENDC}\n")
    for i in range(width + 1):
        percent = (i / width) * 100
        bar = '#' * i + '-' * (width - i)
        sys.stdout.write(f'\r{Colors.BLUE}[{bar}] {percent:.1f}%{Colors.ENDC}')
        sys.stdout.flush()
        time.sleep(duration / width)
    print("\n")

def simulate_kill_chain():
    print(f"\n{Colors.BOLD}{Colors.RED}======================================================================{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.RED}  [ RECONSTRUCTION ] APT_BYTETOBREACH :: SIFMIS KILL CHAIN SIMULATOR  {Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.RED}======================================================================{Colors.ENDC}\n")
    
    time.sleep(1)

    # STEP 1: INITIAL INFECTION
    slow_print(f"{Colors.WARNING}[PHASE 1] INITIAL COMPROMISE & INFRASTRUCTURE HOP{Colors.ENDC}")
    slow_print(f"  > Origin: 14 Rothschild Blvd, Tel Aviv, Israel")
    slow_print(f"  > Bounce 1: WireGuard VPN (Frankfurt, DE - 165.22.x.x)")
    slow_print(f"  > Target: Unpatched Linux Gateway (Algeria Ministry Server)")
    simulated_loading_bar("Deploying initial Silver C2 payload via CVE-2023-xxxx", 2.0)
    slow_print(f"{Colors.GREEN}[+] Persistence established on Algerian hop node (uid=0 root).{Colors.ENDC}\n")
    
    # STEP 2: THE API PIVOT
    slow_print(f"{Colors.WARNING}[PHASE 2] THE STERLING BANK PIVOT{Colors.ENDC}")
    slow_print(f"  > Actor scanning subnets from infected Algerian node...")
    time.sleep(1)
    slow_print(f"  > Found open API endpoint: {Colors.CYAN}gazelle-documents-manager-api-prod.sterling.ng{Colors.ENDC}")
    simulated_loading_bar("Brute-forcing legacy API sync tokens", 2.5)
    slow_print(f"{Colors.GREEN}[+] Access GRANTED. Session Token: df19b12c_ACCESSIBLE_OUTLAY_{Colors.ENDC}")
    slow_print(f"  > Lateral movement inside Sterling Bank production cluster successful.\n")

    # STEP 3: MAPPING THE HIERARCHY
    slow_print(f"{Colors.WARNING}[PHASE 3] ACTIVE DIRECTORY ENUMERATION{Colors.ENDC}")
    slow_print("  > Executing custom Node.js Active Directory dump script...")
    time.sleep(0.5)
    
    hierarchies = [
        "CHAIN LEVEL 1: Usman-Rauf (Risk Monitoring)",
        "CHAIN LEVEL 2: Ochemyl (Risk Management)",
        "CHAIN LEVEL 3: Adebayodd (VP Consumer Banking)",
        "CHAIN LEVEL 4: Ukachukwuao (Divisional Head)"
    ]
    
    for h in hierarchies:
        print(f"    {Colors.BLUE}>> Parsed: {h}{Colors.ENDC}")
        time.sleep(0.3)
        
    slow_print(f"\n{Colors.RED}[!] TARGET LOCKED: Abubakar.Suleiman (Managing Director/CEO){Colors.ENDC}\n")

    # STEP 4: DATA EXFILTRATION
    slow_print(f"{Colors.WARNING}[PHASE 4] SIFMIS PAYLOAD EXFILTRATION{Colors.ENDC}")
    slow_print(f"  > Querying ams-1118 for KDSG routing metrics...")
    simulated_loading_bar("Dumping Inter-Bank routing array", 3.0)
    
    # Simulate the raw shell dump output
    json_dump = '{"accountNumber":"3000107794","bankName":"9 PAYMENT SERVICE BANK","currency":"NGN","bic":"IPBNGLA","bankCode":"120001"}...'
    print(f"{Colors.CYAN}{json_dump}{Colors.ENDC}")
    
    slow_print(f"\n{Colors.RED}[CRITICAL] OVERALL EXFILTRATION ESTIMATE: 3TB{Colors.ENDC}")
    slow_print(f"{Colors.RED}[CRITICAL] DATA ROUTED VIA TELEGRAM BOT API -> @ByteToBreach33{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}                    KILL CHAIN SIMULATION COMPLETE                    {Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        simulate_kill_chain()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Simulation aborted by operator.{Colors.ENDC}")
        sys.exit(0)
