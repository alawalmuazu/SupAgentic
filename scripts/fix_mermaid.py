import os

htmlPath = r"c:\Users\OMEN\Documents\remitaplus\dashboard\index.html"

with open(htmlPath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'target((<b>ILYA DZHINELI</b><br>ByteToBreach))': 'target(("<b>ILYA DZHINELI</b><br>ByteToBreach"))',
    'tg[Telegram<br>Marketing]': 'tg["Telegram<br>Marketing"]',
    'stm[Steam & Discord<br>Voice Comms]': 'stm["Steam & Discord<br>Voice Comms"]',
    'dw[Dark Web Forums]': 'dw["Dark Web Forums"]',
    'fraud[FraudKing_234]': 'fraud["FraudKing_234"]',
    'broker[DataBroker_NG]': 'broker["DataBroker_NG"]',
    'bot[@ByteToBreach_bot]': 'bot["@ByteToBreach_bot"]',
    'cash[CashFlow_TLV]': 'cash["CashFlow_TLV"]',
    'trk[TarkovRat_42]': 'trk["TarkovRat_42"]',
    'anime[AnimeShield_01]': 'anime["AnimeShield_01"]',
    'scope[SilentScope_77]': 'scope["SilentScope_77"]',
    'frag[FragMaster_GR]': 'frag["FragMaster_GR"]',
    'urugr[__uru_gr<br>OpSec]': 'urugr["__uru_gr<br>OpSec"]',
    'cvh[CvHNWwEG]': 'cvh["CvHNWwEG"]',
    'ines[inesslopez]': 'ines["inesslopez"]',
    'vtx[DarkVortex_IL]': 'vtx["DarkVortex_IL"]',
    'scan[ScanBot_3000]': 'scan["ScanBot_3000"]',
    'binance((Binance Cluster))': 'binance(("Binance Cluster"))',
    'crypto[CryptoGamer_X]': 'crypto["CryptoGamer_X"]',
    'mmix[MoneroMixer99]': 'mmix["MoneroMixer99"]',
    'ff((FixedFloat XMR))': 'ff(("FixedFloat XMR"))'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(htmlPath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Safely updated HTML via Python UTF-8!")
