import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    __cog_name__ = "ReactionRoles"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.sync_message()
        print(f"DEBUG: ReactionRoles cog načten")

    async def sync_message(self):
        config = self.bot.config
        guild = self.bot.get_guild(config["guild_id"])
        if not guild:
            print("Server nenalezen!")
            return

        channel = guild.get_channel(config["channel_id"])
        if not channel:
            print("Kanál nenalezen!")
            return

        try:
            message = await channel.fetch_message(config["message_id"])
            print(f"DEBUG: Zpráva nalezena! ID={message.id}")
        except discord.NotFound:
            print("DEBUG: Zpráva nebyla nalezena!")
            return

        # Přidat emoji k zprávě, pokud nejsou
        for emoji in config["roles"].keys():
            if not any(str(r.emoji) == emoji for r in message.reactions):
                await message.add_reaction(emoji)
                print(f"DEBUG: Přidáno emoji {emoji}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_reaction(payload, add=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_reaction(payload, add=False)

    async def handle_reaction(self, payload, add=True):
        config = self.bot.config
        if payload.message_id != config["message_id"]:
            return

        emoji = str(payload.emoji)
        if emoji not in config["roles"]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        role_name = config["roles"][emoji]
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            print(f"DEBUG: Role {role_name} nenalezena!")
            return

        if add:
            await member.add_roles(role)
            await self.send_dm(member, role_name, emoji, added=True)
            print(f"DEBUG: Přidána role {role_name} uživateli {member}")
        else:
            await member.remove_roles(role)
            await self.send_dm(member, role_name, emoji, added=False)
            print(f"DEBUG: Odebrána role {role_name} uživateli {member}")

    async def send_dm(self, member, role_name, emoji, added=True):
        title = "✅ Role přidána" if added else "⚠️ Role odebrána"
        color = 0x1abc9c if added else 0xe74c3c
        description = f"Role **{role_name}** byla {'přidána' if added else 'odebrána'} na serveru **{member.guild.name}**."

        embed = discord.Embed(title=title, description=description, color=color)
        embed.add_field(name="Emoji", value=emoji)
        embed.set_footer(text="Toto je automatická zpráva od ReactionRoles bota")

        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            print(f"DEBUG: Nelze poslat DM uživateli {member}")

    # Synchronizace všech reakcí (pro offline bot)
    async def sync_all(self):
        config = self.bot.config
        guild = self.bot.get_guild(config["guild_id"])
        if not guild:
            print("SYNC: Guild nenalezena!")
            return
        channel = guild.get_channel(config["channel_id"])
        if not channel:
            print("SYNC: Channel nenalezen!")
            return
        try:
            message = await channel.fetch_message(config["message_id"])
        except discord.NotFound:
            print("SYNC: Message nenalezena!")
            return

        # Pouze vybrané role s vlastním emoji
        allowed_roles = {
            "<:AP_IT:1021022218999832597>": "AP_IT",
            "<:AP_MA:1021027630738325525>": "AP_MA",
            "<:BIO:1021030484551155762>": "BIO",
            "<:BIO_CH:1021030112390561864>": "BIO_CH",
            "<:BIO_FY:1021029420199832598>": "BIO_FY",
            "<:BIO_MED:1021032056265916496>": "BIO_MED",
            "<:BIO_OBEC:1022495980169478154>": "BIO_OBEC",
            "<:CH:1021030839724822598>": "CH",
            "<:EKO:1021031106293796864>": "EKO",
            "<:FY:102103133711055257": "FY",
            "<:GEO:1021031673980264558>": "GEO",
            "<:MER_TECH:1021032445539274822>": "MER_TECH"
        }

        async def send_dm(member, role_name, emoji_str):
            try:
                dm_embed = discord.Embed(
                    title="✅ Role přidána",
                    description=f"Byla ti přidána role **{role_name}** na serveru **{guild.name}**.",
                    color=0x1abc9c
                )
                dm_embed.add_field(name="Emoji", value=emoji_str)
                dm_embed.set_footer(text="Toto je automatická zpráva od ReactionRoles bota")
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                print(f"Nelze poslat DM uživateli {member}")

        for emoji_str, role_name in allowed_roles.items():
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                print(f"SYNC: Role {role_name} nenalezena!")
                continue

            # Najít reakci podle vlastního emoji
            reaction = None
            for r in message.reactions:
                if str(r.emoji) == emoji_str:
                    reaction = r
                    break

            reacted_users = [u.id async for u in reaction.users() if not u.bot] if reaction else []
            members_with_role = [m.id for m in role.members]

            # Přidat roli těm, kdo zareagovali, ale roli nemají
            for user_id in reacted_users:
                if user_id not in members_with_role:
                    member = guild.get_member(user_id)
                    if member is None:
                        print(f"Uživatel s ID {user_id} nenalezen v cache.")
                        continue
                    await member.add_roles(role)
                    await send_dm(member, role_name, emoji_str)
                    print(f"SYNC: Přidána role {role_name} uživateli {member}")

        print("SYNC dokončen! Přidány pouze nové role podle reakcí.")






    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_roles(self, ctx):
        guild = ctx.guild
        removed_roles = []
        for emoji, role_name in self.bot.config["roles"].items():
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                for member in role.members:
                    await member.remove_roles(role)
                    removed_roles.append(f"{member} -> {role.name}")
                    await self.send_dm(member, role.name, emoji, added=False)
        await ctx.send(f"✅ Reaction-role role byly odebrány všem uživatelům.\n```{chr(10).join(removed_roles)}```")


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
