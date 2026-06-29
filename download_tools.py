import urllib.request
import zipfile
import os

tools_dir = r"C:\Users\OMEN\Documents\SupAgentic\tools"
os.makedirs(tools_dir, exist_ok=True)

urls = {
    "nuclei.zip": "https://github.com/projectdiscovery/nuclei/releases/download/v3.9.0/nuclei_3.9.0_windows_amd64.zip",
    "caido.zip": "https://storage.googleapis.com/caido-releases/v0.39.0/caido-cli-v0.39.0-windows-x86_64.zip"
}

for filename, url in urls.items():
    filepath = os.path.join(tools_dir, filename)
    print(f"[*] Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"[+] Download complete: {filename}")
        
        extract_dir = os.path.join(tools_dir, filename.replace('.zip', '_bin'))
        print(f"[*] Extracting to {extract_dir}...")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"[+] Extraction complete: {filename}")
    except Exception as e:
        print(f"[-] Error processing {filename}: {e}")
