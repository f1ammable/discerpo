import discord
import capstone
from discord import app_commands
from discord.ext import commands
import os
import typing
#import requests - replace with aiohttp to asynchronously download files

# Own custom module imports
#import disasm
from botToken import token # Not stealing my token

# Create the files directory which the binaries will be stored in

if os.path.isdir('files'):
    os.chdir('files')
else:
    os.mkdir('files') and os.chdir('files')

# Set up bot

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    await bot.load_extension('jishaku') # just to sync guild commands, will be done manually later
    print("running")

@bot.hybrid_command(name="disasm", description="Dissasembles file provided", usage="disasm <architecture>, <bitmode {32,64}>, <file>, <function  {Optional}>")
@app_commands.guilds(discord.Object(id=964964494772166756)) # Currently only for custom guild to not deal with waiting for sync
async def disassemble(ctx: commands.context, arch: str, bitmode: int, file: discord.Attachment, func: typing.Optional[str]):
    if not file:
        if not ctx.message.attachments:
            await ctx.send("Please attach a file")
        file = ctx.message.attachments[0].url
    # Download the file and save it to /files
bot.run(token)