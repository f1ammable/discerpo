import discord
import capstone
from discord.ext import commands
import os
#import requests - replace with aiohttp to asynchronously download files

# Own custom module imports
#import disasm
from botToken import token # Not stealing my token

bot = commands.Bot(command_prefix="$")
os.chdir('files')
    
@bot.event
async def on_ready():
    print("Logged in")

@bot.command()
async def disassemble(ctx, file): #provide function name potentially to only disassemble by function 
    try:
        r = requests.get(file, allow_redirects=True)
        open(f"{ctx.author.id}", 'wb').write(r.content)
        await ctx.send(f'File has been downloaded')
    except:
        await ctx.send("Please provide a url")
    
@bot.command()    
async def deleteDownloadedFile(ctx):
    try:
        os.remove(f'{ctx.author.id}')
        await ctx.send(f'Deleted file {ctx.author.id}')
    except:
        await ctx.send("File not found")

bot.run(token)
#TODO: Implement these commands as the new discord slash commands