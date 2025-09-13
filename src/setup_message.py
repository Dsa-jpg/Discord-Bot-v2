import discord
from discord.ext import commands
import yaml
import os
from dotenv import load_dotenv

# Načtení tokenu z .env
load_dotenv()
TOKEN = os.getenv("DISCORD_KEY")

# Cesta ke configu
CONFIG_PATH = "src/config/config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

CHANNEL_ID = config["channel_id"]
GUILD_ID = config["guild_id"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    # Embed zpráva
    embed = discord.Embed(
        title="🎓 Vítejte na serveru PřF JCU!",
        description="Pro přístup do samostatných roomek pro váš obor reagujte na tuto zprávu příslušným emoji.\n\n"
                    "Každé emoji odpovídá jednomu oboru. Reagujte pouze jednou pro váš obor.",
        color=0x1abc9c
    )

    # Oddělení kategorií
    section1 = {
    "<:AP_IT:1021022218999832597>": "AP_IT",
    "<:AP_MA:1021027630738325525>": "AP_MA",
    "<:BIO_FY:1021029420191993898>": "BIO_FY",
    "<:BIO_CH:1021030112390561864>": "BIO_CH",
    "<:BIO:1021030484551155762>": "BIO",
    "<:BIO_OBEC:1022495980169478154>": "BIO_OBEC"
}

    section2 = {
    "<:CH:1021030839724822598>": "CH",
    "<:EKO:1021031106293796864>": "EKO",
    "<:FY:1021031337110552587>": "FY",
    "<:GEO:1021031673980264558>": "GEO",
    "<:BIO_MED:1021032056265916496>": "BIO_MED",
    "<:MER_TECH:1021032445539274822>": "MER_TECH"
}


    # Přidání polí embed – sekce 1
    embed.add_field(name="🧪 Sekce 1", value="\n".join([f"{k} {v}" for k, v in section1.items()]), inline=True)
    # Přidání polí embed – sekce 2
    embed.add_field(name="🔬 Sekce 2", value="\n".join([f"{k} {v}" for k, v in section2.items()]), inline=True)

    embed.set_footer(text="Pokud nějaká role chybí, kontaktujte @Filip Nachtman")

    # Odeslání zprávy
    message = await channel.send(embed=embed)
    print(f"Zpráva odeslána, ID: {message.id}")

    # Uložení message_id do configu
    config["message_id"] = message.id
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)
    print("message_id uložen do config.yaml")

    await bot.close()  # Ukončení bota po odeslání zprávy

if __name__ == "__main__":
    bot.run(TOKEN)
