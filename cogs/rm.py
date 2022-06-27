import discord
from discord import app_commands
from discord.ext import commands
import os


class Remove_File(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    @app_commands.command(name="rm_file", description="Deletes stored binary")
    @app_commands.guilds(discord.Object(id=964964494772166756))
    async def deleteFile(self, interaction: discord.Interaction):
            filesDir = os.listdir(".")
            if len(filesDir) == 0:
                await interaction.response.send_message("There are no files stored")
            else:
                for f in filesDir:
                    if f.startswith(f'{interaction.user.id}'):
                            os.remove(f)
                            await interaction.response.send_message("File deleted")
                    else:
                        await interaction.response.send_message("File does not exist")


async def setup(bot):
    await bot.add_cog(Remove_File(bot))
