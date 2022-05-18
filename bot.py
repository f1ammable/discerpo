import discord
from discord import app_commands
from discord.ext import commands
import os
import typing
#import requests - replace with aiohttp to asynchronously download files

# Own custom module imports
#import disasm
from botToken import token # Not stealing my token
import download

# Create the files directory which the binaries will be stored in

if os.path.isdir('files'):
    os.chdir('files')
else:
    os.mkdir('files') 
    os.chdir('files')

# Set up bot

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    await bot.load_extension('jishaku') # just to sync guild commands, will be done manually later
    print("running")

@bot.hybrid_command(name="disasm", description="Dissasembles attachement provided", usage="disasm <architecture>, <bit mode {32, 64}>, <file>, <function  {Optional}>")
@app_commands.guilds(discord.Object(id=964964494772166756)) # Currently only for custom guild to not deal with waiting for sync
async def disassembleFile(ctx: commands.context, arch: str, bitmode: int, file: discord.Attachment, func: typing.Optional[str]):
    if not file:
            await ctx.send("File attachement missing")
    file = ctx.message.attachments[0].url
    await ctx.send(await download.download(file, ctx.author.id))

@bot.hybrid_command(name="disasm_url", description="Dissasembles file provided from URL", usage="disasm <architecture>, <bitmode {32,64}>, <file url>, <function  {Optional}>")
@app_commands.guilds(discord.Object(id=964964494772166756))
async def dissasembleURL(ctx: commands.context, arch: str, bitmode: int, file: str, func: typing.Optional[str]):
    if not file:
        await ctx.send("Please provide file url")

@bot.hybrid_command(name="rm_file", description="Deletes stored binary")
@app_commands.guilds(discord.Object(id=964964494772166756))
async def deleteFile(ctx : commands.context):
    try:
        os.remove(ctx.author.id)
        await ctx.send("File deleted")
    except:
        await ctx.send("File does not exist")

bot.run(token)