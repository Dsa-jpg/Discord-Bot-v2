import sys
import os
import discord
from discord.ext import commands
import yaml
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()
TOKEN = os.getenv("DISCORD_KEY")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config["prefix"], intents=intents)
        self.config = config

    async def setup_hook(self):
        await self.load_extension("cogs.reaction_roles")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")
    cog = bot.get_cog("ReactionRoles")
    if cog:
        print("Spouštím sync všech reakcí...")
        await cog.sync_all()
        
        # Pokud chceš, smaž zprávy po sync
        channel = bot.get_channel(config["channel_id"])
        message = await channel.fetch_message(config["message_id"])
        print("SYNC dokončen")

    await bot.close()  # Ukončí bota po dokončení

if __name__ == "__main__":
    bot.run(TOKEN)
