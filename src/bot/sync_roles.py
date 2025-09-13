import asyncio
import discord
import yaml
import os
from cogs.reaction_roles import ReactionRoles
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_KEY")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
bot.config = config

async def main():
    await bot.login(TOKEN)
    cog = ReactionRoles(bot)
    await cog.sync_all()  # Přímo spustí sync
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
