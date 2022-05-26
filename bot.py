import discord
from discord import app_commands
from discord.ext import commands
import os
import typing
import aiohttp
import aiofiles
from pathlib import Path
import glob

# Own custom module imports
#import disasm
from botToken import token # Not stealing my token
import disasm

# Create the files directory which the binaries will be stored in

if os.path.isdir('files'):
    os.chdir('files')
else:
    os.mkdir('files') 
    os.chdir('files')

# Set up bot

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!', owner_id=865159891491618836)

async def download(url, filename): # Downloading files 
    async with aiohttp.ClientSession() as s: # Use bot.session in the future
        async with s.get(url) as r:
            if r.status == 200:
                f = await aiofiles.open(f'{filename}', mode='wb')
                await f.write(await r.read())
                await f.close()
    return Path(str(filename)).absolute()  

@bot.event
async def on_ready():
    await bot.load_extension('jishaku') # just to sync guild commands, will be done manually later
    print("running")

#Bot commands which can be accessed by users

@bot.hybrid_command(name="disasm", description="Disassembles attachement provided", usage="disasm <architecture>, <bit mode {32, 64}>, <file>, <function  {Optional}>")
@app_commands.guilds(discord.Object(id=964964494772166756)) # Currently only for custom guild to not deal with waiting for sync
async def disassembleFile(ctx: commands.context, arch: str, bitmode: str, file: discord.Attachment, func: typing.Optional[str]):
    if not file:
        await ctx.send("File attachement missing")
    newFile = await download(ctx.message.attachments[0].url, str(ctx.author.id))
    await ctx.send(file = await disasm.processFile(newFile, "lol", "lol"), content="Here's your disassembled file")

@bot.hybrid_command(name="disasm_url", description="Disassembles file provided from URL", usage="disasm <architecture>, <bitmode {32,64}>, <file url>, <function  {Optional}>")
@app_commands.guilds(discord.Object(id=964964494772166756))
async def disassembleURL(ctx: commands.context, arch: str, bitmode: str, file: str, func: typing.Optional[str]):
    if not file:
        await ctx.send("Please provide file url")

@bot.hybrid_command(name="rm_file", description="Deletes stored binary")
@app_commands.guilds(discord.Object(id=964964494772166756))
async def deleteFile(ctx : commands.context):
    try:
        for file in glob.glob(f'{ctx.author.id}*'):
            os.remove(file)
        await ctx.send("File deleted")
    except:
        await ctx.send("File does not exist")

@bot.command()
@commands.is_owner()
async def timer(ctx: commands.context):
    pass # make a performance counter and sync command usable by owner only
        # remove jishaku after this is done
        
bot.run(token)