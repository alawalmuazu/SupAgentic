import os
import re

html_path = r"c:\Users\OMEN\Documents\remitaplus\dashboard\index.html"

# Files to inject
target_files = [
    r"c:\Users\OMEN\.gemini\antigravity\brain\765a3496-9a55-477b-bc09-71c786f45359\04_public_advisory.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\765a3496-9a55-477b-bc09-71c786f45359\05_threat_actor_profile.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\06_eureka_intelligence_playbook.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\07_raw_intelligence_dump.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\08_hyper_specific_telemetry.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\09_connecting_the_dots.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\10_social_network_map.md",
    r"c:\Users\OMEN\.gemini\antigravity\brain\2cd0ca13-3970-4c22-a4a1-639f4b0d6c79\11_executive_master_report.md"
]

colors = ["#fff", "#00e5ff", "#00ff9d", "#ff3b5c", "#6b52ff", "#ffb86c", "#00e5ff", "#ff3b5c", "#00ff9d"]

generated_html = """
    <section class="tab-panel" id="tab-dossiers">
      <div class="card card-warn" style="border-color: #00e5ff;">
        <h2 class="card-title" style="color: #00e5ff;">📂 MASTER ARCHIVE: COMPLETE UNREDACTED OPERATION DOSSIER</h2>
        <p class="warn-text">UNFILTERED RAW DATA. This section contains every single intelligence artifact, report, and tracker generated across Operation REMITA-EUREKA.</p>
      </div>
      <div class="grid-2col" style="margin-top: 1rem;">
"""

for idx, filepath in enumerate(target_files):
    # Try .resolved first, then fallback to .md
    actual_path = filepath + ".resolved"
    if not os.path.exists(actual_path):
        actual_path = filepath
        
    if os.path.exists(actual_path):
        with open(actual_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Escape HTML characters in markdown so standard <pre> rendering doesn't break
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
        filename = os.path.basename(actual_path).replace('.resolved', '')
        color = colors[idx % len(colors)]
        
        generated_html += f"""
        <div class="card" style="background: #0a0a10; border-left: 4px solid {color};">
          <h2 class="card-title" style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: {color};">[FILE: {filename}]</h2>
          <pre style="white-space: pre-wrap; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #8892b0; overflow-x: auto; max-height: 450px; overflow-y: scroll; padding: 1rem; background: #000; border-radius: 4px; border: 1px solid #333;">{content}</pre>
        </div>
        """
    else:
        print(f"[!] Warning: File not found: {actual_path}")
        
generated_html += """
      </div>
    </section>
"""

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Using regex to replace everything from <section class="tab-panel" id="tab-dossiers"> to the matching </section>
pattern = re.compile(r'<section class="tab-panel" id="tab-dossiers">.*?</section>', re.DOTALL)

if pattern.search(text):
    new_text = pattern.sub(generated_html, text)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Dashboard updated successfully!")
else:
    print("Could not find the target section in index.html")
