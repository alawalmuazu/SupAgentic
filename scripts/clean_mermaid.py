import os

htmlPath = r"c:\Users\OMEN\Documents\remitaplus\dashboard\index.html"

with open(htmlPath, 'r', encoding='utf-8') as f:
    content = f.read()

# Persona Link-Analysis Formats
content = content.replace('B("Ilya Dzhineli")', 'B["Ilya Dzhineli"]')
content = content.replace('C("Bytetobreach33")', 'C["Bytetobreach33"]')
content = content.replace('D("inesslopez")', 'D["inesslopez"]')
content = content.replace('F("Pentesting Ltd")', 'F["Pentesting Ltd"]')
content = content.replace('G("__uru_gr")', 'G["__uru_gr"]')
content = content.replace('I("#OpPedoChat / @TheAnon0ne")', 'I["#OpPedoChat / @TheAnon0ne"]')

content = content.replace('-->|"goga198116"|', '--> |"goga198116"|')
content = content.replace('-->|"Bot Login"|', '--> |"Bot Login"|')
content = content.replace('-.->|"Frankfurt VPS Hosting"|', '-.-> |"Frankfurt VPS Hosting"|')
content = content.replace('-->|"Administrative IP Pivot"|', '--> |"Administrative IP Pivot"|')
content = content.replace('-->|"Tails OS / Kali Linux"|', '--> |"Tails OS / Kali Linux"|')

# Inner Circle Formats
content = content.replace('target(("<b>ILYA DZHINELI</b><br>ByteToBreach"))', 'target["<b>ILYA DZHINELI</b><br>ByteToBreach"]')
content = content.replace('binance(("Binance Cluster"))', 'binance["Binance Cluster"]')
content = content.replace('ff(("FixedFloat XMR"))', 'ff["FixedFloat XMR"]')

with open(htmlPath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mermaid brackets fully sanitized successfully!")
