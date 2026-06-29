import urllib.request, zipfile, os, shutil

caido_dir = r"C:\Users\OMEN\Documents\SupAgentic\tools\caido_bin"
os.makedirs(caido_dir, exist_ok=True)
url = "https://caido.download/releases/v0.57.0/caido-cli-v0.57.0-win-x86_64.zip"
zip_path = os.path.join(caido_dir, "caido.zip")

print(f"[*] Downloading Caido CLI v0.57.0 from {url}...")
try:
    urllib.request.urlretrieve(url, zip_path)
    print(f"[+] Download complete")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(caido_dir)
    print(f"[+] Extracted to {caido_dir}")
    os.remove(zip_path)
    for f in os.listdir(caido_dir):
        print(f"  -> {f}")
except Exception as e:
    print(f"[-] Error: {e}")
