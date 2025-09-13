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
        COGS_PATH = os.path.join(os.path.dirname(__file__), "../cogs")
        for filename in os.listdir(COGS_PATH):
            if filename.endswith(".py") and filename != "__init__.py":
                await self.load_extension(f"cogs.{filename[:-3]}")


bot = MyBot()


@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")


# Manuální příkaz pro synchronizaci rolí
@bot.command(name="sync_roles")
@commands.has_permissions(administrator=True)
async def sync_roles(ctx):
    cog = bot.get_cog("ReactionRoles")
    if not cog:
        await ctx.send("ReactionRoles cog nenalezen!")
        return
    await cog.sync_all()
    await ctx.send("✅ Synchronizace dokončena!")


if __name__ == "__main__":
    bot.run(TOKEN)
