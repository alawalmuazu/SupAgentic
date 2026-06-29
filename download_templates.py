import urllib.request
import zipfile
import os
import shutil

templates_dir = r"C:\Users\OMEN\nuclei-templates"
os.makedirs(templates_dir, exist_ok=True)

url = "https://github.com/projectdiscovery/nuclei-templates/archive/refs/heads/main.zip"
zip_path = os.path.join(templates_dir, "templates.zip")

print(f"[*] Downloading Nuclei templates from {url}...")
try:
    urllib.request.urlretrieve(url, zip_path)
    print(f"[+] Download complete: templates.zip")
    
    print(f"[*] Extracting to {templates_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(templates_dir)
    print(f"[+] Extraction complete.")
    
    # Move files from the 'nuclei-templates-main' subfolder to the root of templates_dir
    extracted_subfolder = os.path.join(templates_dir, "nuclei-templates-main")
    if os.path.exists(extracted_subfolder):
        for item in os.listdir(extracted_subfolder):
            s = os.path.join(extracted_subfolder, item)
            d = os.path.join(templates_dir, item)
            if os.path.exists(d):
                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.remove(d)
            shutil.move(s, d)
        shutil.rmtree(extracted_subfolder)
        print("[+] Files moved to the root of the templates directory.")

except Exception as e:
    print(f"[-] Error processing templates: {e}")
