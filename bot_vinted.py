import discord
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1317712269139906611
VINTED_URL = "https://www.vinted.fr/catalog?brand_ids[]=191646&search_id=18611484916&order=newest_first&page=1"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
seen_items = set()

async def get_current_items():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(VINTED_URL)
        items = await page.query_selector_all('a[href*="/items/"]')

        results = []
        for item in items[:5]:
            url = await item.get_attribute('href')
            title = await item.get_attribute('aria-label') or 'Titre indisponible'
            price = await page.eval_on_selector('.web_ui__Text__muted', 'el => el.innerText')
            results.append({"url": url, "title": title, "price": price})

        await browser.close()
        return results

async def check_vinted():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        current_items = await get_current_items()
        new_items = [(item['title'], item['price'], item['url']) for item in current_items if item['url'] not in seen_items]

        for item in new_items:
            seen_items.add(item[2])
            await channel.send(f"**{item[0]}**\nPrix : {item[1]}\n[Voir l'annonce]({item[2]})")

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"{client.user} est connecté !")
    client.loop.create_task(check_vinted())

client.run(DISCORD_TOKEN)
