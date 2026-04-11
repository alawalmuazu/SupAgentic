import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Listen for console errors
        page.on("console", lambda msg: print(f"CONSOLE {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        
        print("Navigating to http://localhost:8000 ...")
        await page.goto("http://localhost:8000")
        
        # Wait for mermaid to attempt rendering
        await page.wait_for_timeout(3000)
        
        print("Scraping Mermaid SVG text contents (if any error text is rendered):")
        svgs = await page.eval_on_selector_all("svg", "elements => elements.map(e => e.textContent)")
        for svg_text in svgs:
            print("SVG TEXT:", svg_text)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
