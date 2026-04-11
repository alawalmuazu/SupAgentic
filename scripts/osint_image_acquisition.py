"""
============================================================
PRIORITY 1: Self-Service OSINT Image Acquisition
============================================================
Automated image intelligence gathering for subject: Dzhineli, Ilya
Requires: Python 3.10+, requests, beautifulsoup4, Pillow
Install: pip install requests beautifulsoup4 Pillow aiohttp
============================================================
"""

import os
import re
import json
import hashlib
import asyncio
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

# === CONFIGURATION ===
SUBJECT = {
    "name": "Ilya Dzhineli",
    "name_cyrillic": "Илья Джинели",
    "phone_il": "+972526103354",
    "email": "goga198116@gmail.com",
    "vk_id": "id54992101",
    "steam_id": "[U:1:8471923]",
    "steam_id64": "76561198008737651",  # Converted from [U:1:8471923]
    "pinterest": "goga198116",
    "reddit": "Bytetobreach33",
    "twitter": "TheAnon0ne",
    "github_deleted": "uru_sec_gr",
    "domain_expired": "uru.gr",
    "tiktok_1": "cristian_chialva",
    "tiktok_2": "Bytetobreach33",
    "igromania": "goga198116",
    "telegram_handles": ["bytetobreach", "Bytetobreach33", "Bytetobreach_backup"],
}

OUTPUT_DIR = Path("evidence/subject_imagery")
INNER_CIRCLE_DIR = Path("evidence/inner_circle")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def setup_dirs():
    """Create evidence directory structure."""
    for d in [OUTPUT_DIR, INNER_CIRCLE_DIR,
              OUTPUT_DIR / "profile_photos", OUTPUT_DIR / "screenshots",
              OUTPUT_DIR / "wayback", OUTPUT_DIR / "reverse_image",
              OUTPUT_DIR / "metadata"]:
        d.mkdir(parents=True, exist_ok=True)
    print(f"[+] Evidence directories created at: {OUTPUT_DIR.resolve()}")


# ============================================================
# STEP 1: VKontakte Profile Scrape
# ============================================================
def step1_vk_scrape():
    """
    Scrape VKontakte profile for photo albums and tagged photos.
    NOTE: VK API requires access token for full album access.
    This scrapes what's publicly available.
    """
    print("\n" + "="*60)
    print("[STEP 1] VKontakte Profile Scrape")
    print("="*60)

    vk_id = SUBJECT["vk_id"]
    results = {"step": 1, "platform": "VKontakte", "target": vk_id, "images": []}

    # Public profile page
    urls_to_check = [
        f"https://vk.com/{vk_id}",
        f"https://m.vk.com/{vk_id}",  # Mobile version sometimes leaks more
    ]

    # VK API (public, no auth needed for basic info)
    api_url = f"https://api.vk.com/method/users.get?user_ids={vk_id.replace('id','')}&fields=photo_max_orig,photo_400_orig,photo_200,photo_100,has_photo,online,city,country&v=5.199"

    try:
        r = requests.get(api_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "response" in data and len(data["response"]) > 0:
                user = data["response"][0]
                print(f"  [+] Name: {user.get('first_name', '?')} {user.get('last_name', '?')}")
                print(f"  [+] Has Photo: {user.get('has_photo', '?')}")

                for photo_key in ["photo_max_orig", "photo_400_orig", "photo_200", "photo_100"]:
                    if photo_key in user and user[photo_key]:
                        photo_url = user[photo_key]
                        if "camera" not in photo_url and "deactivated" not in photo_url:
                            print(f"  [+] {photo_key}: {photo_url}")
                            results["images"].append({
                                "url": photo_url,
                                "type": photo_key,
                                "source": "VK API"
                            })
                            # Download
                            try:
                                img_r = requests.get(photo_url, headers=HEADERS, timeout=10)
                                if img_r.status_code == 200:
                                    ext = photo_url.split(".")[-1].split("?")[0]
                                    path = OUTPUT_DIR / "profile_photos" / f"vk_{photo_key}.{ext}"
                                    path.write_bytes(img_r.content)
                                    print(f"  [✓] Saved: {path}")
                            except Exception as e:
                                print(f"  [!] Download failed: {e}")
            else:
                print(f"  [!] VK API returned no data or profile is private")
                if "error" in data:
                    print(f"  [!] Error: {data['error'].get('error_msg', 'unknown')}")
        else:
            print(f"  [!] VK API HTTP {r.status_code}")
    except Exception as e:
        print(f"  [!] VK API error: {e}")

    # VK Albums (public)
    albums_url = f"https://api.vk.com/method/photos.getAll?owner_id={vk_id.replace('id','')}&count=200&v=5.199"
    try:
        r = requests.get(albums_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "response" in data:
                items = data["response"].get("items", [])
                print(f"  [+] Found {len(items)} public photos in albums")
                for i, photo in enumerate(items[:20]):  # First 20
                    sizes = photo.get("sizes", [])
                    if sizes:
                        largest = max(sizes, key=lambda s: s.get("width", 0))
                        url = largest.get("url", "")
                        if url:
                            results["images"].append({
                                "url": url,
                                "type": f"album_photo_{i}",
                                "date": photo.get("date", ""),
                                "text": photo.get("text", "")
                            })
    except Exception as e:
        print(f"  [!] VK Albums error: {e}")

    # Save results
    with open(OUTPUT_DIR / "metadata" / "step1_vk.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"  [RESULT] {len(results['images'])} images catalogued")
    return results


# ============================================================
# STEP 2: Truecaller Lookup
# ============================================================
def step2_truecaller():
    """
    Query Truecaller for profile photo.
    NOTE: Truecaller requires Premium API access or manual lookup.
    This documents the process and provides manual instructions.
    """
    print("\n" + "="*60)
    print("[STEP 2] Truecaller Profile Photo Retrieval")
    print("="*60)

    phone = SUBJECT["phone_il"]
    print(f"  [TARGET] Phone: {phone}")
    print(f"  [INFO] Truecaller API requires authentication.")
    print(f"  [MANUAL STEPS]:")
    print(f"    1. Visit https://www.truecaller.com/search/il/{phone.replace('+972', '')}")
    print(f"    2. Or use Truecaller app → search {phone}")
    print(f"    3. Screenshot the profile photo result")
    print(f"    4. Save to: {OUTPUT_DIR / 'profile_photos' / 'truecaller_profile.png'}")
    print(f"  [ALT] Use CallerID apps: Eyecon, Sync.ME, GetContact")

    results = {
        "step": 2, "platform": "Truecaller", "target": phone,
        "status": "MANUAL_REQUIRED",
        "search_urls": [
            f"https://www.truecaller.com/search/il/{phone.replace('+972', '')}",
        ],
        "alt_services": ["Eyecon", "Sync.ME", "GetContact", "Whoscall"]
    }
    with open(OUTPUT_DIR / "metadata" / "step2_truecaller.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# ============================================================
# STEP 3: Reverse Image Search
# ============================================================
def step3_reverse_image():
    """
    Prepare reverse image search queries for any downloaded VK photos.
    Uses Google Lens, TinEye, and Yandex.
    """
    print("\n" + "="*60)
    print("[STEP 3] Reverse Image Search Preparation")
    print("="*60)

    profile_photos = list((OUTPUT_DIR / "profile_photos").glob("*"))
    results = {"step": 3, "searches": []}

    if not profile_photos:
        print("  [!] No profile photos downloaded yet. Run Step 1 first.")
        print("  [!] Or manually save VK/Truecaller photos to profile_photos/")
    else:
        for photo_path in profile_photos:
            print(f"  [+] Preparing searches for: {photo_path.name}")

            # For each image, generate search URLs
            search_entry = {
                "source_image": str(photo_path),
                "search_urls": {
                    "google_lens": "https://lens.google.com/uploadbyurl?url=<upload_image>",
                    "yandex": "https://yandex.com/images/search?rpt=imageview&source=collections",
                    "tineye": "https://tineye.com/search",
                    "pimeyes": "https://pimeyes.com/en (facial recognition - paid)",
                },
                "manual_instructions": [
                    f"1. Go to https://yandex.com/images/ → click camera icon → upload {photo_path.name}",
                    f"2. Go to https://images.google.com → click camera icon → upload {photo_path.name}",
                    f"3. Go to https://tineye.com → upload {photo_path.name}",
                    "4. Document all matching profiles found"
                ]
            }
            results["searches"].append(search_entry)

    # Also search by name
    name_searches = {
        "google": f"https://www.google.com/search?q={quote_plus(SUBJECT['name'])}+photo&tbm=isch",
        "google_cyrillic": f"https://www.google.com/search?q={quote_plus(SUBJECT['name_cyrillic'])}+фото&tbm=isch",
        "yandex_name": f"https://yandex.com/images/search?text={quote_plus(SUBJECT['name_cyrillic'])}",
    }
    results["name_image_searches"] = name_searches
    for label, url in name_searches.items():
        print(f"  [+] {label}: {url}")

    with open(OUTPUT_DIR / "metadata" / "step3_reverse_image.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# ============================================================
# STEP 4: Yandex Facial Search
# ============================================================
def step4_yandex_facial():
    """
    Yandex is superior for CIS (Russian/Eastern European) facial matching.
    """
    print("\n" + "="*60)
    print("[STEP 4] Yandex Facial Recognition Search")
    print("="*60)

    search_url = f"https://yandex.com/images/search?text={quote_plus(SUBJECT['name_cyrillic'])}"
    print(f"  [+] Yandex search: {search_url}")
    print(f"  [MANUAL] Upload PFP-005 (VK partial face) to Yandex Images")
    print(f"  [MANUAL] Also check: Odnoklassniki, Mail.ru, other VK profiles")
    print(f"  [TIP] Yandex reverse image search works much better than Google for CIS faces")

    results = {
        "step": 4, "platform": "Yandex",
        "search_url": search_url,
        "status": "MANUAL_REQUIRED",
        "targets": ["Odnoklassniki", "Mail.ru", "LiveJournal", "VK extended network"]
    }
    with open(OUTPUT_DIR / "metadata" / "step4_yandex.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# ============================================================
# STEP 5: Wayback Machine — uru.gr
# ============================================================
def step5_wayback():
    """
    Check Wayback Machine for archived versions of uru.gr domain.
    Looking for: About pages, team photos, bios from Patras era.
    """
    print("\n" + "="*60)
    print("[STEP 5] Wayback Machine — uru.gr Archive Scan")
    print("="*60)

    domain = SUBJECT["domain_expired"]
    archive_api = f"https://web.archive.org/web/timemap/json?url={domain}&matchType=prefix&collapse=urlkey&output=json&fl=original,timestamp,statuscode&limit=500"

    results = {"step": 5, "domain": domain, "snapshots": [], "images_found": []}

    try:
        r = requests.get(archive_api, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # Skip header row
            snapshots = data[1:] if len(data) > 1 else []
            print(f"  [+] Found {len(snapshots)} Wayback snapshots for {domain}")

            for snap in snapshots[:50]:
                url, timestamp, status = snap[0], snap[1], snap[2]
                if status == "200":
                    wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
                    results["snapshots"].append({
                        "url": url,
                        "wayback_url": wayback_url,
                        "timestamp": timestamp,
                    })
                    # Check for image-heavy pages
                    if any(kw in url.lower() for kw in ["about", "team", "contact", "profile", "bio", "who"]):
                        print(f"  [!] HIGH VALUE: {wayback_url}")
                        results["images_found"].append(wayback_url)

            # Also check the deleted GitHub
            github_archive = f"https://web.archive.org/web/timemap/json?url=github.com/{SUBJECT['github_deleted']}&matchType=prefix&output=json&fl=original,timestamp&limit=100"
            try:
                gr = requests.get(github_archive, headers=HEADERS, timeout=10)
                if gr.status_code == 200:
                    gh_data = gr.json()
                    gh_snaps = gh_data[1:] if len(gh_data) > 1 else []
                    print(f"  [+] Found {len(gh_snaps)} GitHub archive snapshots")
                    for gs in gh_snaps[:20]:
                        wb_url = f"https://web.archive.org/web/{gs[1]}/{gs[0]}"
                        results["snapshots"].append({"url": gs[0], "wayback_url": wb_url, "type": "github"})
            except:
                pass

        else:
            print(f"  [!] Wayback API returned {r.status_code}")
    except Exception as e:
        print(f"  [!] Wayback error: {e}")

    with open(OUTPUT_DIR / "metadata" / "step5_wayback.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"  [RESULT] {len(results['snapshots'])} snapshots, {len(results['images_found'])} high-value pages")
    return results


# ============================================================
# STEP 6: Pinterest Deep Scrape
# ============================================================
def step6_pinterest():
    """
    Scrape Pinterest profile for boards, pins, and potential selfies.
    """
    print("\n" + "="*60)
    print("[STEP 6] Pinterest Profile Scrape")
    print("="*60)

    username = SUBJECT["pinterest"]
    profile_url = f"https://www.pinterest.com/{username}/"
    print(f"  [+] Target: {profile_url}")

    results = {"step": 6, "platform": "Pinterest", "target": username, "boards": []}

    try:
        r = requests.get(profile_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            print(f"  [+] Profile accessible (HTTP 200)")
            # Extract board names from page
            board_pattern = re.findall(r'/"' + username + r'/([^/"]+)/"', r.text)
            unique_boards = list(set(board_pattern))
            print(f"  [+] Found {len(unique_boards)} boards")
            for board in unique_boards[:20]:
                results["boards"].append({
                    "name": board,
                    "url": f"https://www.pinterest.com/{username}/{board}/"
                })
                print(f"    → Board: {board}")
        elif r.status_code == 404:
            print(f"  [!] Profile not found (404)")
        else:
            print(f"  [!] HTTP {r.status_code}")
    except Exception as e:
        print(f"  [!] Pinterest error: {e}")

    with open(OUTPUT_DIR / "metadata" / "step6_pinterest.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# ============================================================
# STEP 13: Steam Friends List Scrape
# ============================================================
def step13_steam_friends():
    """
    Scrape Steam Web API for friends list of the target.
    Steam Web API Key required (free from steamcommunity.com/dev/apikey).
    """
    print("\n" + "="*60)
    print("[STEP 13] Steam Friends List Scrape")
    print("="*60)

    steam_id64 = SUBJECT["steam_id64"]
    api_key = os.environ.get("STEAM_API_KEY", "")

    if not api_key:
        print("  [!] STEAM_API_KEY not set. Get one from:")
        print("      https://steamcommunity.com/dev/apikey")
        print(f"  [MANUAL] Visit: https://steamcommunity.com/profiles/{steam_id64}/friends/")
        results = {"step": 13, "status": "API_KEY_REQUIRED"}
    else:
        friends_url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={api_key}&steamid={steam_id64}"
        results = {"step": 13, "platform": "Steam", "friends": []}

        try:
            r = requests.get(friends_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                friends = data.get("friendslist", {}).get("friends", [])
                print(f"  [+] Found {len(friends)} Steam friends")

                # Get profile details for each friend
                friend_ids = [f["steamid"] for f in friends[:100]]
                batch_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={','.join(friend_ids)}"
                pr = requests.get(batch_url, timeout=10)
                if pr.status_code == 200:
                    players = pr.json().get("response", {}).get("players", [])
                    for player in players:
                        friend_info = {
                            "steam_id": player.get("steamid"),
                            "name": player.get("personaname"),
                            "real_name": player.get("realname", ""),
                            "avatar_full": player.get("avatarfull", ""),
                            "profile_url": player.get("profileurl", ""),
                            "country": player.get("loccountrycode", ""),
                            "last_online": player.get("lastlogoff", ""),
                        }
                        results["friends"].append(friend_info)
                        print(f"    → {friend_info['name']} ({friend_info.get('real_name', '?')}) [{friend_info.get('country', '?')}]")

                        # Download avatar
                        if friend_info["avatar_full"]:
                            try:
                                img_r = requests.get(friend_info["avatar_full"], timeout=5)
                                if img_r.status_code == 200:
                                    avatar_path = INNER_CIRCLE_DIR / f"steam_{player['steamid']}.jpg"
                                    avatar_path.write_bytes(img_r.content)
                            except:
                                pass

                print(f"  [RESULT] {len(results['friends'])} friend profiles + avatars downloaded")
            else:
                print(f"  [!] Steam API returned {r.status_code} — profile may be private")
        except Exception as e:
            print(f"  [!] Steam error: {e}")

    with open(OUTPUT_DIR / "metadata" / "step13_steam.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


# ============================================================
# §7: INNER CIRCLE BATCH SCRAPER
# ============================================================
INNER_CIRCLE = [
    {"alias": "inesslopez", "platforms": ["Exploit.in", "Telegram"], "tier": 1},
    {"alias": "__uru_gr", "platforms": ["Dread", "Greeksec"], "tier": 1},
    {"alias": "CvHNWwEG", "platforms": ["BreachForums", "Telegram"], "tier": 1},
    {"alias": "DarkVortex_IL", "platforms": ["Exploit.in"], "tier": 1},
    {"alias": "Loic_M_FR", "platforms": ["Session"], "tier": 1},
    {"alias": "MoneroMixer99", "platforms": ["Dread", "FixedFloat"], "tier": 2},
    {"alias": "CashFlow_TLV", "platforms": ["Telegram"], "tier": 2},
    {"alias": "SwapKing_NoKYC", "platforms": ["Session"], "tier": 2},
    {"alias": "WireGhost_RU", "platforms": ["VK", "Telegram"], "tier": 2},
    {"alias": "Phantom_Cards", "platforms": ["Dread"], "tier": 2},
    {"alias": "ScanBot_3000", "platforms": ["Telegram"], "tier": 3},
    {"alias": "CloudAudit_X", "platforms": ["Discord"], "tier": 3},
    {"alias": "N1ght_Cr4wl3r", "platforms": ["Dread", "Discord"], "tier": 3},
    {"alias": "InfoSteal_DZ", "platforms": ["Exploit.in"], "tier": 3},
    {"alias": "WHOIS_Ghost", "platforms": ["Session"], "tier": 3},
    {"alias": "DataBroker_NG", "platforms": ["Telegram"], "tier": 4},
    {"alias": "FraudKing_234", "platforms": ["Telegram", "DarkForums"], "tier": 4},
    {"alias": "EU_Privacy_Leak", "platforms": ["Dread"], "tier": 4},
    {"alias": "BankPwn_SC", "platforms": ["Session"], "tier": 4},
    {"alias": "AirMiles_UZ", "platforms": ["BreachForums"], "tier": 4},
    {"alias": "TarkovRat_42", "platforms": ["Steam", "Discord"], "tier": 5},
    {"alias": "FragMaster_GR", "platforms": ["Steam"], "tier": 5},
    {"alias": "SilentScope_77", "platforms": ["Steam", "Faceit"], "tier": 5},
    {"alias": "CryptoGamer_X", "platforms": ["Steam", "Telegram"], "tier": 5},
    {"alias": "AnimeShield_01", "platforms": ["Steam", "Discord"], "tier": 5},
]

def batch_inner_circle_scrape():
    """
    Batch process all 25 inner circle contacts.
    For each: Sherlock scan → profile scrape → reverse image → store.
    """
    print("\n" + "="*60)
    print("[§7] INNER CIRCLE BATCH IMAGE ACQUISITION")
    print("="*60)

    all_results = []

    for contact in INNER_CIRCLE:
        alias = contact["alias"]
        tier = contact["tier"]
        print(f"\n  [CONTACT {INNER_CIRCLE.index(contact)+1}/25] {alias} (Tier {tier})")

        contact_dir = INNER_CIRCLE_DIR / alias
        contact_dir.mkdir(parents=True, exist_ok=True)

        result = {
            "alias": alias,
            "tier": tier,
            "platforms": contact["platforms"],
            "sherlock_hits": [],
            "images_found": [],
        }

        # Sherlock-style platform check (surface web)
        surface_platforms = {
            "github": f"https://github.com/{alias}",
            "reddit": f"https://www.reddit.com/user/{alias}",
            "twitter": f"https://twitter.com/{alias}",
            "instagram": f"https://www.instagram.com/{alias}/",
            "tiktok": f"https://www.tiktok.com/@{alias}",
            "pinterest": f"https://www.pinterest.com/{alias}/",
            "pastebin": f"https://pastebin.com/u/{alias}",
            "keybase": f"https://keybase.io/{alias}",
            "steam": f"https://steamcommunity.com/id/{alias}",
            "vk": f"https://vk.com/{alias}",
        }

        for platform, url in surface_platforms.items():
            try:
                r = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    result["sherlock_hits"].append({
                        "platform": platform,
                        "url": url,
                        "status": "FOUND"
                    })
                    print(f"    [✓] {platform}: {url}")
            except:
                pass

        # Save contact results
        with open(contact_dir / "scan_results.json", "w") as f:
            json.dump(result, f, indent=2)

        all_results.append(result)

    # Summary
    total_hits = sum(len(r["sherlock_hits"]) for r in all_results)
    print(f"\n  [SUMMARY] Scanned 25 contacts. Found {total_hits} surface web hits.")

    with open(INNER_CIRCLE_DIR / "batch_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    return all_results


# ============================================================
# MASTER EXECUTION
# ============================================================
def run_all():
    """Execute all available automated steps."""
    print("╔" + "═"*58 + "╗")
    print("║  OSINT IMAGE ACQUISITION PROTOCOL — AUTOMATED RUNNER   ║")
    print("║  Subject: Ilya Dzhineli (Илья Джинели)                 ║")
    print(f"║  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                          ║")
    print("╚" + "═"*58 + "╝")

    setup_dirs()

    # Priority 1: Self-Service
    print("\n\n" + "▓"*60)
    print("  PRIORITY 1: SELF-SERVICE OSINT")
    print("▓"*60)

    r1 = step1_vk_scrape()
    r2 = step2_truecaller()
    r3 = step3_reverse_image()
    r4 = step4_yandex_facial()
    r5 = step5_wayback()
    r6 = step6_pinterest()

    # Priority 3: Steam
    print("\n\n" + "▓"*60)
    print("  PRIORITY 3: ADVANCED — STEAM NETWORK")
    print("▓"*60)

    r13 = step13_steam_friends()

    # §7: Inner Circle
    print("\n\n" + "▓"*60)
    print("  §7: INNER CIRCLE BATCH PROCESS")
    print("▓"*60)

    batch_results = batch_inner_circle_scrape()

    # Final Report
    print("\n\n" + "═"*60)
    print("  EXECUTION COMPLETE")
    print("═"*60)
    print(f"  Evidence stored at: {OUTPUT_DIR.resolve()}")
    print(f"  Inner circle at:    {INNER_CIRCLE_DIR.resolve()}")
    print(f"  Manual steps remaining:")
    print(f"    → Step 2: Truecaller Premium lookup")
    print(f"    → Step 3: Upload photos to reverse image search engines")
    print(f"    → Step 4: Yandex facial search with VK profile photo")
    print(f"    → Steps 7-12: Law enforcement coordination required")


if __name__ == "__main__":
    run_all()
