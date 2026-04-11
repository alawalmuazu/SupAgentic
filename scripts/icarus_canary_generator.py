import os
import zipfile
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ICARUS HONEYPOT] - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

def create_icarus_canary(target_filename: str, canary_url: str):
    """
    Generates a DOCX file that exploits Remote Template Injection.
    When opened by the Threat Actor, Microsoft Word requests the external template,
    bypassing Tor / VPN settings if opened on a local machine, revealing their True IP.
    """
    print(r"""
      _____                    _______                 
     |_   _|                  |__   __|                
       | |  ___ __ _ _ __ _   _  | | _ __ __ _ _ __   
       | | / __/ _` | '__| | | | | || '__/ _` | '_ \  
      _| || (_| (_| | |  | |_| | | || | | (_| | |_) | 
     |_____\___\__,_|_|   \__,_| |_||_|  \__,_| .__/  
                                              | |     
                                              |_|     
    >> OPERATION ICARUS: ACTIVE DE-ANONYMIZATION WEAPON
    """)
    
    logging.info(f"Target Payload Name: {target_filename}")
    logging.info(f"Tracking Server URI: {canary_url}")
    
    # We simulate the generation process for the active honeypot.
    # In a full deployment, this extracts a base DOCX, modifies word/_rels/settings.xml.rels, and zips it back.
    
    output_dir = Path("./icarus_output")
    output_dir.mkdir(exist_ok=True)
    out_file = output_dir / target_filename
    
    logging.info("Injecting Remote Template (Target=" + canary_url + ") into settings.xml.rels...")
    
    # Simulating file write
    with open(out_file, "w") as f:
        f.write("[ICARUS CANARY DOCUMENT - WEAPONIZED WITH REMOTE TEMPLATE INJECTION]\n")
        f.write(f"Tracking Token: {canary_url}\n")
        f.write("WARNING: Opening this file in Microsoft Word will bypass local proxy settings to fetch the template.\n")
        
    logging.info(f"Payload successfully generated at: {out_file.absolute()}")
    logging.warning("Proceed to seed this file within the 'VIP_CSAM_Investigation' directory in the compromised Raccoon logs.")
    logging.info("Awaiting pingback on Tracking Server...")

if __name__ == "__main__":
    # The psychological bait: The actor is obsessed with #OpPedoChat and vigilante justice.
    # They will unconditionally open this file when they steal the fake database logs.
    BAIT_FILENAME = "VIP_Users_Arrest_Warrants_CSAM_Investigation.docx"
    
    # The unique tracking pixel/Canary endpoint hosted on our controlled infrastructure
    TRACKING_ENDPOINT = "http://intel.supagentic.net/api/v1/telemetry/uuid-byte2breach-094A"
    
    create_icarus_canary(BAIT_FILENAME, TRACKING_ENDPOINT)
