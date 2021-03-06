import discord
from discord.ext import commands
import os
import errors

# Easier to manage a token across different machines
token = os.getenv('DISCORD')

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
    
@bot.event
async def on_ready():
    for f in os.listdir("../cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs."+f[:-3])
            errors.logger.info(f'Extension cogs.{f[:-3]} loaded')
    await bot.load_extension('jishaku')  # just to sync guild commands, will be done manually later
    errors.logger.warning('Bot is running')

bot.run(token)
