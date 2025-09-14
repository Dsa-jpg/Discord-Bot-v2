import sys, os, discord, yaml
from discord.ext import commands
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
        cog = self.get_cog("ReactionRoles")
        if cog:
            print("Spouštím automatický sync všech reakcí...")
            await cog.sync_all()
            print("SYNC dokončen a log odeslán!")
        else:
            print("Cog ReactionRoles nebyl nalezen!")
        await self.close()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")

if __name__ == "__main__":
    bot.run(TOKEN)
