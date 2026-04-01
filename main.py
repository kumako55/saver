import asyncio
import aiohttp
import requests
import os
import threading
import time
from fastapi import FastAPI
import uvicorn

# Logs ko real-time dikhane ke liye
os.environ["PYTHONUNBUFFERED"] = "1"

app = FastAPI()

# Configuration
PROXY_SOURCE = "https://sunny9577.github.io/proxy-scraper/proxies.txt"
RAW_FILE = "raw_proxies.txt"
WORKING_FILE = "working_proxies.txt"
REFRESH_INTERVAL = 3 * 60 * 60  # 3 Ghante (Seconds mein)

@app.get("/")
def status():
    alive_count = 0
    if os.path.exists(WORKING_FILE):
        with open(WORKING_FILE, "r") as f:
            alive_count = len(f.readlines())
    
    return {
        "status": "Proxy Engine Active",
        "proxies_found_alive": alive_count,
        "next_refresh_in": "Check logs for countdown"
    }

async def test_proxy(session, proxy_addr):
    """Proxy ko Google par test karne ka function"""
    proxy_url = f"http://{proxy_addr}"
    try:
        async with session.get("http://www.google.com", proxy=proxy_url, timeout=7) as resp:
            if resp.status == 200:
                return proxy_addr
    except:
        return None
    return None

async def proxy_engine():
    print("🚀 Starting Proxy Engine (3-Hour Cycle)...", flush=True)
    
    while True:
        try:
            # 1. Fetching Proxies from Website
            print(f"📥 Fetching fresh proxies from {PROXY_SOURCE}...", flush=True)
            r = requests.get(PROXY_SOURCE, timeout=15)
            new_proxies = list(set(r.text.splitlines()))
            
            # 2. Save to Local Storage (Raw)
            with open(RAW_FILE, "w") as f:
                for p in new_proxies:
                    f.write(f"{p}\n")
            print(f"💾 Saved {len(new_proxies)} raw proxies to {RAW_FILE}", flush=True)

            # 3. Parallel Testing (Alive Check)
            print("⚡ Starting Parallel Testing...", flush=True)
            connector = aiohttp.TCPConnector(limit=150) # Render ke liye 150 connections safe hain
            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = [test_proxy(session, p) for p in new_proxies]
                results = await asyncio.gather(*tasks)
            
            # 4. Filter and Save Alive Proxies
            working = [r for r in results if r is not None]
            with open(WORKING_FILE, "w") as f:
                for p in working:
                    f.write(f"{p}\n")
            
            print(f"✅ Check Complete! Found {len(working)} Alive proxies.", flush=True)
            print(f"😴 Next fetch in 3 hours...", flush=True)

        except Exception as e:
            print(f"⚠️ Engine Error: {str(e)[:50]}", flush=True)
        
        # 3 Ghante ka wait
        await asyncio.sleep(REFRESH_INTERVAL)

def run_checker_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(proxy_engine())

if __name__ == "__main__":
    # Checker ko background thread mein chalao
    threading.Thread(target=run_checker_thread, daemon=True).start()
    
    # Render ke port par API chalao
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
