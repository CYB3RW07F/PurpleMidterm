import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='start')
async def start(ctx):
    await ctx.send('Ik leef? Ik leef!')

bot.run(os.getenv("BOT_TOKEN"))