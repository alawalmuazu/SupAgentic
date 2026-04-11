import uuid
import datetime
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SupAgentic Defensive Operations] - %(levelname)s - %(message)s')

class CanaryGenerator:
    """
    SupAgentic Blue Team Module: Passive Canary Token Generator
    Generates a tracking beacon designed to be hidden inside internal organizational 
    databases (like KDSG SIFMIS). It operates strictly defensively.
    """
    
    def __init__(self, target_network="KDSG_SIFMIS_VLAN"):
        self.target_network = target_network
        self.canary_id = str(uuid.uuid4())
        self.deployment_time = datetime.datetime.now().isoformat()

    def generate_fake_database_beacon(self):
        """
        Creates a tracking URL that looks like a high-value internal resource.
        """
        logging.info(f"Generating defensive tracking beacon for {self.target_network}...")
        
        # Simulating a Thinkst Canary / Custom AWS API Gateway tracking endpoint
        tracking_url = f"https://api.kdsg-sifmis-internal.gov.ng/v2/payroll/export?token={self.canary_id}"
        
        fake_csv_content = f"""EMPLOYEE_ID,FIRST_NAME,LAST_NAME,ACCOUNT_NUMBER,BANK_ID,ROUTING_URL
90812,Sani,Abubakar,0019283741,STERLING, {tracking_url}
90813,Fatima,Bello,0019283742,STERLING, {tracking_url}
90814,Admin,ServiceAccount,---,---, {tracking_url}"""

        logging.info("✅ SUCCESS: Fake SIFMIS payroll CSV generated with embedded tracking beacons.")
        logging.warning("INSTRUCTION: Do not send this to the threat actor. Inject this file silently into the KDSG SIFMIS internal file share.")
        logging.info("If the actor breaches the network again and downloads this file, opening it or clicking the URL will instantly trigger an alert with their real IP Address and Browser Fingerprint.")
        
        return fake_csv_content

if __name__ == "__main__":
    print("\n--- SupAgentic Passive Honeypot System ---")
    generator = CanaryGenerator()
    payload = generator.generate_fake_database_beacon()
    print("\n[Generated Payload Preview - sifmis_payroll_q3.csv]")
    print(payload)
    print("------------------------------------------\n")
