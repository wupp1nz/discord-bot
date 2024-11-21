import discord
from discord.ext import commands
from config import *
from games import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, description="Test Bot for discord.py", intents=intents)
MESSAGEID = 797355209558327357


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    print("I am alive!")


@bot.command(pass_context=True)
async def hello(ctx, name: str):
    await ctx.send(f"Welcome {name}")


@bot.event
async def on_raw_reaction_add(payload):
    if MESSAGEID == payload.message_id:
        guild = await bot.fetch_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        emoji = payload.emoji.name
        role = None
        if emoji == "🎮":
            role = discord.utils.get(guild.roles, name="Gamer")

        if role and member:
            await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if MESSAGEID == payload.message_id:
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        emoji = payload.emoji.name
        role = None
        if emoji == "🎮":
            role = discord.utils.get(guild.roles, name="Gamer")

        if role and member:
            await member.remove_roles(role)


@bot.command(pass_context=True)
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) + 1))


@bot.command(pass_context=True)
async def game(ctx):
    await LoadGames(ctx, bot)

bot.run(TOKEN)
