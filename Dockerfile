# 1. Lightweight Python image use kar rahe hain
FROM python:3.9-slim

# 2. Working directory set karein
WORKDIR /app

# 3. Logs ko real-time dikhane ke liye environment variable
ENV PYTHONUNBUFFERED=1

# 4. Requirements ko Docker ke andar hi install karein (Alag file ki zaroorat nahi)
RUN pip install --no-cache-dir \
    aiohttp \
    requests \
    fastapi \
    uvicorn

# 5. Aapka main.py file copy karein
COPY main.py .

# 6. Render ka default port expose karein
EXPOSE 10000

# 7. Bot start karne ki command
CMD ["python", "main.py"]
