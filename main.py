import asyncio
import random
import requests
import os
import threading
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async  # Corrected Import
from fastapi import FastAPI
import uvicorn
from fake_useragent import UserAgent

# Environment settings
os.environ["PYTHONUNBUFFERED"] = "1"
app = FastAPI()
ua = UserAgent()

# Configuration
SMART_LINK = "https://www.profitablecpmratenetwork.com/hp7r6v2y?key=cc271770a7de081b727acf154507ebe2"
PROXY_SOURCE = "https://sunny9577.github.io/proxy-scraper/proxies.txt"

@app.get("/")
def health(): 
    return {"status": "Asad's Full-Spoof Bot is Active"}

async def human_behavior(page):
    """Asli insan ki tarah scroll aur mouse movement simulate karna"""
    try:
        # Random scrolling
        for _ in range(random.randint(2, 5)):
            await page.mouse.wheel(0, random.randint(300, 600))
            await asyncio.sleep(random.uniform(2.0, 5.0))
        
        # Random mouse movement (Fake coordinates)
        await page.mouse.move(random.randint(100, 700), random.randint(100, 700))
    except: 
        pass

async def visit_logic():
    print("🛡️ Booting Bot with Full Spoofing & Stealth...", flush=True)
    
    async with async_playwright() as p:
        # Browser launch with evasive arguments to bypass detection
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox", 
            "--disable-setuid-sandbox", 
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-dev-shm-usage" # Render ki kam RAM ke liye zaroori
        ])
        
        while True:
            p_addr = "N/A"
            context = None
            try:
                # 1. Fresh Proxy Fetch
                r = requests.get(PROXY_SOURCE, timeout=10)
                proxies = r.text.splitlines()
                if not proxies:
                    print("⚠️ No proxies found, waiting 30s...", flush=True)
                    await asyncio.sleep(30)
                    continue
                    
                p_addr = random.choice(proxies).strip()
                
                # 2. Setup Context with Fake Identity (High Spoofing)
                context = await browser.new_context(
                    proxy={"server": f"http://{p_addr}"},
                    user_agent=ua.random,
                    viewport={'width': random.randint(1280, 1920), 'height': random.randint(720, 1080)},
                    device_scale_factor=random.choice([1, 2]),
                    locale=random.choice(["en-US", "en-GB", "en-CA", "en-AU"])
                )

                page = await context.new_page()
                
                # 3. Apply Stealth (Playwright detection hide karta hai)
                await stealth_async(page) 
                
                # 4. Block Images & CSS (Render 512MB RAM Fix)
                await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff,ttf,svg}", lambda route: route.abort())

                # 5. Visit Smart Link
                print(f"🚀 Visiting via Proxy: {p_addr}", flush=True)
                await page.goto(SMART_LINK, wait_until="domcontentloaded", timeout=60000)
                
                # 6. Human Behavior (Impression quality barhanay ke liye)
                await human_behavior(page)
                
                # Stay on page for 45-80 seconds (Critical for Revenue)
                stay = random.randint(45, 85)
                print(f"✅ Page Loaded! Staying for {stay}s...", flush=True)
                await asyncio.sleep(stay)
                
                await context.close()
                
            except Exception as e:
                # Error handle kar ke loop chalta rahega
                err_msg = str(e).split('\n')[0] # Pehli line error ki
                print(f"⚠️ Proxy {p_addr} Failed: {err_msg}", flush=True)
                if context:
                    await context.close()
            
            # Memory release break
            await asyncio.sleep(random.randint(10, 20))

def run_bg():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(visit_logic())

if __name__ == "__main__":
    # Background thread mein bot chalayen
    threading.Thread(target=run_bg, daemon=True).start()
    # FastAPI port setting for Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
