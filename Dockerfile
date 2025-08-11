FROM python:3.11-slim

# Dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    chromium     chromium-driver     fonts-liberation     ca-certificates     && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Por defecto ejecuta el script principal
CMD ["python", "main.py"]
