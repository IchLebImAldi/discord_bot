import discord
from discord.ext import commands

class info_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="help", help="Informations about this bot")
    async def h(self, ctx):
       await ctx.send("Help")