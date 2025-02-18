# Dockerfile pour bot Discord Vinted sur Railway
FROM python:3.12-slim

# Installation des dépendances nécessaires pour Playwright et Chromium
RUN apt-get update && apt-get install -y wget curl unzip fontconfig locales libc6 libglib2.0-0 libnss3 libatk1.0-0 libcups2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libxshmfence1

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer les navigateurs Playwright
RUN npx playwright install --with-deps

# Lancer le bot
CMD ["python", "bot_vinted.py"]
