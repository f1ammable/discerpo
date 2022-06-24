import discord
from discord import app_commands
from discord.ext import commands
import typing

import backend
import errors


class Disasm_command(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    @app_commands.command(name="disasm", description="Disassembles attachment or URL provided")
    @app_commands.guilds(discord.Object(id=964964494772166756))  # Currently only syncing to my personal server for testing as to not wait up to 24 hours for a command sync
    async def disassembleFile(self, interaction: discord.Interaction, attachment: typing.Optional[discord.Attachment], url: typing.Optional[str]):  # typing.Union doesn't seem to work for this unfortunately
        if isinstance(attachment, discord.Attachment):
            downloadedFile = await backend.download(interaction.namespace.attachment.url, str(interaction.user.id), self.bot)
            disassembled_file = await backend.processFile(downloadedFile)  
            await interaction.response.send_message(file=disassembled_file, content="Here's your disassembled file")

        elif isinstance(url, str):
                downloadedFile = await backend.download(url, str(interaction.user.id), self.bot)
                disassembled_file = await backend.processFile(downloadedFile)
                await interaction.response.send_message(file=disassembled_file, content="Here's your disassembled file")

    @disassembleFile.error
    async def disasm_err(self, interaction: discord.Interaction, error):
        if isinstance(error, errors.InvalidMagic): # Does not actually send the message
            await interaction.response.send_message("Invalid magic bytes in file provided. Please try again")


async def setup(bot):
    await bot.add_cog(Disasm_command(bot))
