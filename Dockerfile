FROM python:3.12-slim

# Evita prompts en apt
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    chromium \
    chromium-driver \
    fonts-liberation \
    xvfb \
    ca-certificates \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Variables para que Selenium/Chrome sepan dónde está
ENV CHROME_BIN=/usr/bin/chromium \
TZ=Europe/Madrid

WORKDIR /app

# Requisitos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Por si generas logs/salidas
VOLUME ["/out"]

# Por defecto ejecuta el script principal
CMD ["python", "main.py"]
