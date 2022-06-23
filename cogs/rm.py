import discord
from discord import app_commands
from discord.ext import commands
import glob
import os


class Remove_File(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    @commands.hybrid_command(name="rm_file", description="Deletes stored binary")
    @app_commands.guilds(discord.Object(id=964964494772166756))
    async def deleteFile(self, ctx: commands.context):
        try:
            for file in glob.glob(f'{ctx.author.id}*'):
                os.remove(file)
            await ctx.send("File deleted")
        except:
            await ctx.send("File does not exist")


async def setup(bot):
    await bot.add_cog(Remove_File(bot))
