import os
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Directories
EVIDENCE_DIR = Path("c:/Users/OMEN/Documents/SupAgentic/scripts/evidence/inner_circle")
AVATARS_DIR = EVIDENCE_DIR / "avatars_downloaded"
AVATARS_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def download_image(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"      [!] Failed to download image: {e}")
    return False

def extract_og_image(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for og:image
            og_img = soup.find("meta", property="og:image")
            if og_img and og_img.get("content"):
                return og_img["content"]
            
            # Look for twitter:image
            tw_img = soup.find("meta", name="twitter:image")
            if tw_img and tw_img.get("content"):
                return tw_img["content"]
                
            # Steam specific profile avatar
            if "steamcommunity" in url:
                avatar = soup.find("div", class_="playerAvatarAutoSizeInner")
                if avatar and avatar.find("img"):
                    return avatar.find("img")["src"]
                    
            # Reddit specific
            if "reddit.com" in url:
                img_tag = soup.select_one('img[alt*="avatar"]')
                if img_tag and img_tag.get("src"):
                    return img_tag["src"]
                    
    except Exception as e:
        print(f"      [!] Error parsing {url}: {e}")
    return None

def main():
    print("="*60)
    print("  INNER CIRCLE AVATAR EXTRACTOR")
    print("="*60)
    
    total_downloaded = 0
    total_checked = 0
    
    # Iterate through all JSON files in the inner_circle directories
    for root, dirs, files in os.walk(EVIDENCE_DIR):
        for file in files:
            if file == "scan_results.json":
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    
                alias = data.get("alias", "Unknown")
                print(f"\n[+] Processing: {alias}")
                
                alias_dir = AVATARS_DIR / alias
                alias_dir.mkdir(exist_ok=True)
                
                hits = data.get("sherlock_hits", [])
                for hit in hits:
                    platform = hit.get("platform")
                    url = hit.get("url")
                    total_checked += 1
                    
                    print(f"  -> Scraping {platform} ({url})")
                    
                    # Instagram/TikTok block heavily, but we'll try reddit/steam/pinterest/etc
                    if platform in ["instagram", "tiktok"]:
                        print("      [~] Skipping (Cloudflare/Login wall expected)")
                        continue
                        
                    img_url = extract_og_image(url)
                    if img_url:
                        print(f"      [✓] Found Avatar URL: {img_url}")
                        ext = img_url.split(".")[-1].split("?")[0][:4]
                        if not ext.isalpha(): ext = "jpg"
                        
                        save_name = alias_dir / f"{platform}_avatar.{ext}"
                        
                        if download_image(img_url, save_name):
                            print(f"      [+] Downloaded: {save_name.name}")
                            total_downloaded += 1
                    else:
                        print(f"      [-] No avatar found or blocked by captcha/WAF.")
                        
                    time.sleep(1) # Be polite
                    
    print("="*60)
    print(f"  COMPLETE! Downloaded {total_downloaded} avatars out of {total_checked} links.")
    print(f"  Saved to: {AVATARS_DIR}")

if __name__ == "__main__":
    main()
