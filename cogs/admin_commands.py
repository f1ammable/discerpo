import discord
from discord import app_commands
from discord.ext import commands


class Admin_Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__()

    # @commands.command(name="timer")
    # @commands.is_owner()
    # async def timer(self, ctx: commands.context):
    #     pass # TODO: make a performance counter and sync command usable by owner only
    #         # remove jishaku after this is done

    # @commands.command(name="sync")
    # @commands.is_owner() # WIP sync command
    # async def commandSync(self, ctx: commands.context):
    #     try:
    #         await self.bot.tree.sync(discord.Object(id=964964494772166756))
    #         await ctx.send("Commands synced")
    #     except:
    #         await ctx.send("Something went wrong")

    @app_commands.command(name="reload", description="reloads specified module")
    @commands.is_owner()
    @app_commands.guilds(discord.Object(id=964964494772166756))
    async def reload(self, interaction: discord.Interaction, module: str):
        try:
            await self.bot.unload_extension(f'cogs.{module}')
            await self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await interaction.response.send_message('{}: {}'.format(type(e).__name__, e))
        else:
            await interaction.response.send_message(f'reloaded `cogs.{module}`')


async def setup(bot):
    await bot.add_cog(Admin_Commands(bot))
