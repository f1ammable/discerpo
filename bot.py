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
bot = commands.Bot(intents=intents, command_prefix='!')
bot.session = None

async def getSession(bot): # Don't create new aiohttp.Clientsession() everytime
    if bot.session is None:
        bot.session = aiohttp.ClientSession()
    return bot.session

async def download(url, filename): # Downloading files
    async with await getSession(bot) as s: 
        async with s.get(url) as r:
            if r.status == 200:
                f = await aiofiles.open(f'{filename}', mode='wb')
                await f.write(await r.read())
                await f.close()
            else:
                return "Invalid url provided"
    return Path(str(filename)).absolute()

@bot.event
async def on_ready():
    await bot.load_extension('jishaku') # just to sync guild commands, will be done manually later
    print("running")

#Bot commands which can be accessed by users

@bot.hybrid_command(name="disasm", description="Disassembles attachement or URL provided")
@app_commands.guilds(discord.Object(id=964964494772166756)) # Currently only syncing to my personal server for testing as to not wait up to 24 hours for a command sync 
async def disassembleFile(ctx: commands.context, arch: str, bitmode: str, attachment: typing.Optional[discord.Attachment], url: typing.Optional[str]): # typing.Union doesn't seem to work for this unfortunately
    if isinstance(attachment, discord.Attachment):
        downloadedFile = await download(ctx.message.attachments[0].url, str(ctx.author.id))
        await ctx.send(file = await disasm.processFile(downloadedFile, arch, bitmode), content = "Here's your disassembled file")
    elif isinstance(url, str):
        try:
            downloadedFile = await download(url, str(ctx.author.id))
            await ctx.send(file = await disasm.processFile(downloadedFile, arch, bitmode), content="Here's your disassembled file")
        except:
            await ctx.send("Something went wrong")
    else:
        await ctx.send("Please provide a file url or attachement")

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

@bot.command()
@commands.is_owner() # trying to make a sync command - currently guild only
async def commandSync(ctx: commands.context):
    try:
        await bot.tree.sync(discord.Object(id=964964494772166756))
        await ctx.send("Commands synced")
    except:
        await ctx.send("Something went wrong")
bot.run(token)