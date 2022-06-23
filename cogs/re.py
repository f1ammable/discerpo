import discord
from discord import app_commands
from discord.ext import commands
import typing

import backend


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

            if isinstance(disassembled_file, discord.File):  # Another isinstance check if processFile returns an exception due to an incompatible file
                await interaction.response.send_message(file=disassembled_file, content="Here's your disassembled file")
            else:
                await interaction.response.send_message(disassembled_file)
        elif isinstance(url, str):
            try:
                downloadedFile = await backend.download(url, str(interaction.user.id), self.bot)
                disassembled_file = await backend.processFile(downloadedFile)

                if isinstance(disassembled_file, discord.File):
                    await interaction.response.send_message(file=disassembled_file, content="Here's your disassembled file")
                else:
                    await interaction.response.send_message(disassembled_file)
            except Exception as e:
                await interaction.response.send_message(f'{type(e).__name__}: {e}')
        else:
            await interaction.response.send_message("Please provide a file url or attachment")


async def setup(bot):
    await bot.add_cog(Disasm_command(bot))
