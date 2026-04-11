import os
import json
import asyncio
from pathlib import Path
from urllib.parse import urlparse
import requests

EVIDENCE_DIR = Path("c:/Users/OMEN/Documents/SupAgentic/scripts/evidence/inner_circle")
AVATARS_DIR = EVIDENCE_DIR / "avatars_downloaded"
AVATARS_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def download_image(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return True
    except:
        pass
    return False

async def extract_avatars():
    from playwright.async_api import async_playwright
    
    # We will target 10 high-value failed nodes to prove execution speed
    targets = [
        "DarkVortex_IL", "CashFlow_TLV", "FraudKing_234", "TarkovRat_42", "WireGhost_RU",
        "ScanBot_3000", "InfoSteal_DZ", "EU_Privacy_Leak", "MoneroMixer99", "DataBroker_NG"
    ]
    
    print("="*60)
    print("  PLAYWRIGHT ADVANCED EXTRACTION ENGINE")
    print("="*60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        for alias in targets:
            json_file = EVIDENCE_DIR / alias / "scan_results.json"
            if not json_file.exists(): continue
                
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            print(f"\n[+] Injecting Headless Bypass for: {alias}")
            alias_dir = AVATARS_DIR / alias
            alias_dir.mkdir(exist_ok=True)
            
            for hit in data.get("sherlock_hits", []):
                platform = hit.get("platform")
                url = hit.get("url")
                
                # Try Reddit first as it's common and heavily WAF'd
                if platform == "reddit":
                    print(f"  -> Bypassing JS check: {url}")
                    page = await context.new_page()
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                        # Wait an extra second for Reddit React to render
                        await page.wait_for_timeout(1500)
                        
                        # Grab og:image
                        og_img = await page.evaluate('() => { const meta = document.querySelector("meta[property=\'og:image\']"); return meta ? meta.content : null; }')
                        
                        if og_img:
                            print(f"      [\u2713] Extracted payload: {og_img}")
                            ext = og_img.split(".")[-1].split("?")[0][:4]
                            if not ext.isalpha(): ext = "jpg"
                            if download_image(og_img, alias_dir / f"{platform}_avatar_pw.{ext}"):
                                print(f"      [+] Captured!")
                        else:
                            print("      [-] Shadowbanned or empty avatar.")
                    except Exception as e:
                        print(f"      [!] Timeout/Blocks")
                    finally:
                        await page.close()
                        
        await browser.close()
        
if __name__ == "__main__":
    asyncio.run(extract_avatars())
