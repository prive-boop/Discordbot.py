import discord
from discord.ext import commands
import json
import os
import random
import asyncio

TOKEN = "MTUwMTkwMzYxMDAwMTQ5MDAwMA.GlgnRM.xMYCChi8G_dTYzl4ijszWqbwcFRoWJuAIhg7A4"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# VERIFY BUTTON
# =========================

class VerifyView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        role = discord.utils.get(
            interaction.guild.roles,
            name="Verified"
        )

        if role is None:

            await interaction.response.send_message(
                "Verified role bestaat niet.",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(role)

        await interaction.response.send_message(
            "Je bent verified!",
            ephemeral=True
        )

# =========================
# TICKET BUTTON
# =========================

class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Open Ticket",
        style=discord.ButtonStyle.blurple,
        custom_id="ticket_button"
    )
    async def ticket_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        guild = interaction.guild

        existing = discord.utils.get(
            guild.channels,
            name=f"ticket-{interaction.user.name}"
        )

        if existing:

            await interaction.response.send_message(
                "Je hebt al een ticket.",
                ephemeral=True
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        await channel.send(
            f"{interaction.user.mention} welkom in je ticket."
        )

        await interaction.response.send_message(
            f"Ticket gemaakt: {channel.mention}",
            ephemeral=True
        )

# =========================
# READY EVENT
# =========================

@bot.event
async def on_ready():

    bot.add_view(VerifyView())
    bot.add_view(TicketView())

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash commands geladen")
    except Exception as e:
        print(e)

    print(f"Online als {bot.user}")

# =========================
# WELCOME MESSAGE
# =========================

@bot.event
async def on_member_join(member):

    channel = discord.utils.get(
        member.guild.text_channels,
        name="welcome"
    )

    if channel:

        embed = discord.Embed(
            title="Welkom",
            description=f"{member.mention} joined de server!",
            color=discord.Color.green()
        )

        await channel.send(embed=embed)

# =========================
# LOGS
# =========================

@bot.event
async def on_message_delete(message):

    if message.author.bot:
        return

    channel = discord.utils.get(
        message.guild.text_channels,
        name="logs"
    )

    if channel:

        embed = discord.Embed(
            title="Message Deleted",
            description=message.content,
            color=discord.Color.red()
        )

        embed.add_field(
            name="User",
            value=message.author.mention
        )

        await channel.send(embed=embed)

# =========================
# /PING
# =========================

@bot.tree.command(
    name="ping",
    description="Bot ping"
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"Pong! {latency}ms"
    )

# =========================
# /VERIFYPANEL
# =========================

@bot.tree.command(
    name="verifypanel",
    description="Send verify panel"
)
async def verifypanel(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Verify",
        description="Klik hieronder om te verifyen.",
        color=discord.Color.green()
    )

    await interaction.channel.send(
        embed=embed,
        view=VerifyView()
    )

    await interaction.response.send_message(
        "Verify panel gestuurd.",
        ephemeral=True
    )

# =========================
# /TICKETPANEL
# =========================

@bot.tree.command(
    name="ticketpanel",
    description="Send ticket panel"
)
async def ticketpanel(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Tickets",
        description="Klik hieronder om een ticket te openen.",
        color=discord.Color.blue()
    )

    await interaction.channel.send(
        embed=embed,
        view=TicketView()
    )

    await interaction.response.send_message(
        "Ticket panel gestuurd.",
        ephemeral=True
    )

# =========================
# /POLL
# =========================

@bot.tree.command(
    name="poll",
    description="Create a poll"
)
async def poll(
    interaction: discord.Interaction,
    question: str
):

    embed = discord.Embed(
        title="Poll",
        description=question,
        color=discord.Color.orange()
    )

    msg = await interaction.channel.send(
        embed=embed
    )

    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

    await interaction.response.send_message(
        "Poll gemaakt.",
        ephemeral=True
    )

# =========================
# /SAY
# =========================

@bot.tree.command(
    name="say",
    description="Laat bot praten"
)
async def say(
    interaction: discord.Interaction,
    message: str
):

    await interaction.channel.send(message)

    await interaction.response.send_message(
        "Verzonden.",
        ephemeral=True
    )

# =========================
# /EMBED
# =========================

@bot.tree.command(
    name="embed",
    description="Maak embed"
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    description: str
):

    emb = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    await interaction.channel.send(embed=emb)

    await interaction.response.send_message(
        "Embed gestuurd.",
        ephemeral=True
    )

# =========================
# /PURGE
# =========================

@bot.tree.command(
    name="purge",
    description="Delete messages"
)
async def purge(
    interaction: discord.Interaction,
    amount: int
):

    await interaction.channel.purge(
        limit=amount
    )

    await interaction.response.send_message(
        f"{amount} berichten verwijderd.",
        ephemeral=True
    )

# =========================
# /KICK
# =========================

@bot.tree.command(
    name="kick",
    description="Kick member"
)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "Geen reden"
):

    await member.kick(reason=reason)

    await interaction.response.send_message(
        f"{member.mention} kicked."
    )

# =========================
# /BAN
# =========================

@bot.tree.command(
    name="ban",
    description="Ban member"
)
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "Geen reden"
):

    await member.ban(reason=reason)

    await interaction.response.send_message(
        f"{member.mention} banned."
    )

# =========================
# /GIVEAWAY
# =========================

@bot.tree.command(
    name="giveaway",
    description="Start giveaway"
)
async def giveaway(
    interaction: discord.Interaction,
    prize: str
):

    embed = discord.Embed(
        title="🎉 GIVEAWAY 🎉",
        description=f"Prize: {prize}\n\nReact met 🎉",
        color=discord.Color.gold()
    )

    msg = await interaction.channel.send(
        embed=embed
    )

    await msg.add_reaction("🎉")

    await interaction.response.send_message(
        "Giveaway gestart.",
        ephemeral=True
    )

# =========================
# /SERVERINFO
# =========================

@bot.tree.command(
    name="serverinfo",
    description="Server info"
)
async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(
        title=guild.name,
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Members",
        value=guild.member_count
    )

    embed.add_field(
        name="Channels",
        value=len(guild.channels)
    )

    embed.add_field(
        name="Roles",
        value=len(guild.roles)
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /BACKUP
# =========================

@bot.tree.command(
    name="backup",
    description="Backup server"
)
async def backup(interaction: discord.Interaction):

    guild = interaction.guild

    data = {
        "roles": [],
        "channels": []
    }

    for role in guild.roles:

        data["roles"].append(role.name)

    for channel in guild.channels:

        data["channels"].append({
            "name": channel.name,
            "type": str(channel.type)
        })

    with open(
        f"{guild.id}.json",
        "w"
    ) as f:

        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        "Backup opgeslagen."
    )

# =========================
# START BOT
# =========================

bot.run(TOKEN)
