import discord
from discord import app_commands
from discord.ext import commands
import typing

# Own module imports
import dl
import disasm

class Disasm_command(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    @commands.hybrid_command(name="disasm", description="Disassembles attachement or URL provided")
    @app_commands.guilds(discord.Object(id=964964494772166756)) # Currently only syncing to my personal server for testing as to not wait up to 24 hours for a command sync 
    async def disassembleFile(self, ctx: commands.context, attachment: typing.Optional[discord.Attachment], url: typing.Optional[str]): # typing.Union doesn't seem to work for this unfortunately
        if isinstance(attachment, discord.Attachment):
            downloadedFile = await dl.download(ctx.message.attachments[0].url, str(ctx.author.id), self.bot)
            disassembled_file = await disasm.processFile(downloadedFile)

            if isinstance(disassembled_file, discord.File): # Anoter isintance check if processFile returns an exception due to an incompatible file
                await ctx.send(file = disassembled_file, content = "Here's your disassembled file")
            else:
                await ctx.send(disassembled_file)
        elif isinstance(url, str):
            try:
                downloadedFile = await dl.download(url, str(ctx.author.id), self.bot)
                disassembled_file = await disasm.processFile(downloadedFile)

                if isinstance(disassembled_file, discord.File):
                    await ctx.send(file = disassembled_file, content="Here's your disassembled file")
                else:
                    await ctx.send(disassembled_file)
            except Exception as e:
                await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send("Please provide a file url or attachement")

async def setup(bot):
    await bot.add_cog(Disasm_command(bot))