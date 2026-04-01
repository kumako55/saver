# Step 1: Python ka latest slim version use karein
FROM python:3.10-slim

# Step 2: System updates aur wget (browser install karne ke liye)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Step 3: Saari Requirements yahan install ho rahi hain
RUN pip install --no-cache-dir \
    playwright \
    playwright-stealth \
    fastapi \
    uvicorn \
    requests \
    fake-useragent

# Step 4: Playwright ka browser aur uski dependencies (Fix for Exit Code 100)
RUN playwright install chromium
RUN playwright install-deps chromium

# Step 5: Code copy karein
COPY . .

# Step 6: Render ka default port
EXPOSE 10000

# Step 7: Bot run karein
CMD ["python", "main.py"]
