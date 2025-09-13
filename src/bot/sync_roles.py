import sys
import os
import asyncio
import discord
import yaml
from dotenv import load_dotenv

# Přidání root projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cogs.reaction_roles import ReactionRoles

load_dotenv()
TOKEN = os.getenv("DISCORD_KEY")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
bot.config = config

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")
    cog = ReactionRoles(bot)
    await cog.sync_all(add_only=True)  # jen přidání chybějících rolí
    print("SYNC dokončen, bot se zavírá")
    await bot.close()

asyncio.run(bot.start(TOKEN))
