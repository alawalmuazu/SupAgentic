import re

htmlPath = r"c:\Users\OMEN\Documents\remitaplus\dashboard\index.html"

with open(htmlPath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix mermaid tags - unescape HTML entities inside div.mermaid
def unescape_mermaid(match):
    block = match.group(0)
    block = block.replace('&gt;', '>')
    block = block.replace('&lt;', '<')
    block = block.replace('&amp;', '&')
    return block

content = re.sub(r'<div class="mermaid".*?>.*?</div>', unescape_mermaid, content, flags=re.DOTALL)

# Add Mermaid initialize if missing
init_script = "<script>mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });</script>"
if init_script not in content:
    content = content.replace("</body>", f"  {init_script}\n</body>")

with open(htmlPath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Systematic DOM un-escaping and initialization successfully injected.")
