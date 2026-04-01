import asyncio
import random
import requests
import os
import threading
from playwright.async_api import async_playwright
from playwright_stealth import stealth as apply_stealth
from fastapi import FastAPI
import uvicorn
from fake_useragent import UserAgent

os.environ["PYTHONUNBUFFERED"] = "1"
app = FastAPI()
ua = UserAgent()

# Configuration
SMART_LINK = "https://www.profitablecpmratenetwork.com/hp7r6v2y?key=cc271770a7de081b727acf154507ebe2"
PROXY_SOURCE = "https://sunny9577.github.io/proxy-scraper/proxies.txt"

@app.get("/")
def health(): return {"status": "Full-Spoof Bot Active"}

async def human_behavior(page):
    """Asli insan ki tarah scroll aur mouse hilana"""
    try:
        # Random scrolling
        for _ in range(random.randint(3, 6)):
            await page.mouse.wheel(0, random.randint(200, 500))
            await asyncio.sleep(random.uniform(1.5, 4.0))
        
        # Random mouse movement
        await page.mouse.move(random.randint(0, 500), random.randint(0, 500))
    except: pass

async def visit_logic():
    print("🛡️ Booting Bot with Full Spoofing & Stealth...", flush=True)
    
    async with async_playwright() as p:
        # Browser launch with evasive arguments
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox", 
            "--disable-setuid-sandbox", 
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars"
        ])
        
        while True:
            p_addr = "N/A"
            try:
                # 1. Fresh Proxy Fetch
                r = requests.get(PROXY_SOURCE, timeout=10)
                proxies = r.text.splitlines()
                p_addr = random.choice(proxies)
                
                # 2. Setup Context with Fake Identity
                context = await browser.new_context(
                    proxy={"server": f"http://{p_addr}"},
                    user_agent=ua.random,
                    viewport={'width': random.randint(1024, 1920), 'height': random.randint(720, 1080)},
                    device_scale_factor=random.choice([1, 2]),
                    is_mobile=False,
                    has_touch=False,
                    locale=random.choice(["en-US", "en-GB", "en-CA"])
                )

                page = await context.new_page()
                
                # 3. Apply Stealth (Hides Playwright Fingerprints)
                await apply_stealth(page)
                
                # 4. Block Tracker-Heady Resources to save RAM
                await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff,ttf,svg}", lambda route: route.abort())

                # 5. Visit with Timeout
                print(f"🚀 Visiting via Proxy: {p_addr}", flush=True)
                await page.goto(SMART_LINK, wait_until="domcontentloaded", timeout=60000)
                
                # 6. Act like a Human (Very Important for Adsterra)
                await human_behavior(page)
                
                # Wait for Impression (High CPM requires staying time)
                stay = random.randint(45, 80)
                print(f"✅ Loaded! Staying for {stay}s...", flush=True)
                await asyncio.sleep(stay)
                
                await context.close()
                
            except Exception as e:
                print(f"⚠️ Proxy {p_addr} Failed: {str(e)[:40]}", flush=True)
                try: await context.close()
                except: pass
            
            # Memory safety break
            await asyncio.sleep(random.randint(5, 15))

def run_bg():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(visit_logic())

if __name__ == "__main__":
    threading.Thread(target=run_bg, daemon=True).start()
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
