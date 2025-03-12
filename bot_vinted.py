import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import asyncio

# Charger les variables d'environnement depuis le fichier .env
load_dotenv("test.env")

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("Le token Discord est manquant. Vérifie le fichier .env")

CHANNEL_ID = 1317712269139906611  # ID de votre channel Discord
VINTED_URL = "https://www.vinted.fr/catalog?brand_ids[]=191646&search_id=18611484916&order=newest_first&page=1"

# Initialisation du bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Selenium Options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0")

seen_items = set()  # Suivi des URLs pour éviter les doublons

def get_current_items(driver):
    """Récupère toutes les annonces actuellement visibles sur la page."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/items/"]'))
        )
        script = """
        let items = document.querySelectorAll('a[href*="/items/"]');
        return Array.from(items).map(item => {
            let title = item.querySelector('img')?.alt || 
                        item.querySelector('h3')?.innerText || 
                        Array.from(item.childNodes).map(n => n.textContent.trim()).filter(Boolean).join(' ') || 
                        'Titre indisponible';
            
            // Recherche précise du prix avec une classe identifiée
            let priceElement = item.closest('.feed-grid__item, .feed-item').querySelector('p.web_ui__Text__text.web_ui__Text__muted');
            let price = priceElement ? priceElement.innerText.trim() : 'Prix non spécifié';
            
            return {
                url: item.href,
                title: title,
                price: price
            };
        });
        """
        return driver.execute_script(script)
    except Exception as e:
        print(f"Erreur lors de la récupération des annonces : {e}")
        return []

async def check_vinted():
    """Vérifie et envoie les nouvelles annonces sur Discord en rafraîchissant constamment la page."""
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    print("Démarrage du bot pour surveiller les nouvelles annonces Vinted...")

    try:
        with webdriver.Chrome(options=options) as driver:
            while True:
                driver.get(VINTED_URL)
                print("Page Vinted actualisée...")

                current_items = get_current_items(driver)
                new_items = []

                for item in current_items[:5]:  # Limite aux 5 dernières annonces
                    url = item["url"]
                    title = item["title"]
                    price = item["price"]
                    if url not in seen_items:
                        seen_items.add(url)
                        new_items.append((title, price, url))

                # Envoyer les nouvelles annonces
                if new_items:
                    print(f"{len(new_items)} nouvelle(s) annonce(s) trouvée(s). Envoi sur Discord...")
                    for title, price, url in new_items:
                        message = (
                            f"====================\n"
                            f"**💼 Titre : {title}**\n"
                            f"💰 Prix : {price}\n"
                            f"🔗 [Voir l'annonce ici]({url})\n"
                            f"===================="
                        )
                        await channel.send(message)
                else:
                    print("Aucune nouvelle annonce détectée.")

                await asyncio.sleep(1)
    except Exception as e:
        print(f"Erreur principale : {e}")

@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !")
    client.loop.create_task(check_vinted())
async def on_disconnect():
    print("Le bot s'est déconnecté, tentative de reconnexion...")

# Lancer le bot
client.run(DISCORD_TOKEN)
