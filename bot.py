import discord
import capstone
from discord.ext import commands
#import disasm
from COOLBOT import botToken
import os
import requests

bot = commands.Bot(command_prefix="$")
wd = os.getcwd()

def check(author):
    def inner(msg):
        if msg.author != author:
            return False    
        else:
            return True
    

@bot.event
async def on_ready():
    print("Logged in")

@bot.command()
async def fooTest(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def disassemble(ctx, file, arch, codeType, funcName): #funcName optional lol
    if file is None:
        await bot.wait_for('attachement', check=check(ctx.author), timeout=30)
    elif file != None:
        for atch in ctx.message.attachements:
            await atch[0].save(f"{wd}/files/{atch.filename}")

@bot.command()
async def fileDownloadURL(ctx, url):
    r = requests.get(url, allow_redirects=True)
    open(f"{ctx.author.id}", 'wb').write(r.content)

bot.run(botToken)