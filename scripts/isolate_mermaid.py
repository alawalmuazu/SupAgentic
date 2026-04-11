import asyncio
from playwright.async_api import async_playwright
import os

html_template = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });</script>
</head>
<body>
    <div class="mermaid">
        %s
    </div>
</body>
</html>
"""

tests = [
"""graph TD
A["+972 52 610 3354 Israel Cellcom"] --> B["Ilya Dzhineli"]
B -->|goga198116| C["Bytetobreach33"]
C --- D["inesslopez"]
D -->|Bot Login| E["Algerian Infostealer Raccoon StealC"]
C -->|Frankfurt VPS Hosting| F["Pentesting Ltd"]
F -->|Administrative IP Pivot| G["OpSec uru_gr"]
G -->|Tails OS Kali Linux| H["Greek Origin Node"]
G --> I["OpPedoChat TheAnon0ne"]

classDef CDef1 fill:#1a1a26,stroke:#ff3b5c,stroke-width:2px,color:#e4e4ef
classDef CDef2 fill:#22222f,stroke:#ff8c42
class A,E,H CDef2
""",
"""graph TD
A["972 52 610 3354 Israel Cellcom"] --> B["Ilya Dzhineli"]
B -->|goga198116| C["Bytetobreach33"]
C --- D["inesslopez"]
D -->|Bot Login| E["Algerian Infostealer"]
C -->|Frankfurt VPS Hosting| F["Pentesting Ltd"]
F -->|Administrative IP Pivot| G["OpSec uru_gr"]
G -->|Tails OS Kali Linux| H["Greek Origin Node"]
G --> I["OpPedoChat TheAnon0ne"]
""",
"""graph TD
A["NodeA"] --> B["NodeB"]
"""
]

async def check_graph(index, graph_text):
    html_path = f"test_{index}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template % graph_text)
    
    html_abs = "file:///" + os.path.abspath(html_path).replace('\\', '/')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Capture console errors
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto(html_abs)
        await page.wait_for_timeout(2000)
        
        svgs = await page.eval_on_selector_all("svg", "elements => elements.map(e => e.textContent)")
        is_error = any("Syntax error" in text for text in svgs) or len(svgs) == 0
        
        print(f"Test {index}: {'CRASHED' if is_error else 'SUCCESS'}")
        if is_error:
            print(f"   Errors: {errors}")
            
        await browser.close()
        
async def main():
    for idx, t in enumerate(tests):
        await check_graph(idx, t)

if __name__ == "__main__":
    asyncio.run(main())
