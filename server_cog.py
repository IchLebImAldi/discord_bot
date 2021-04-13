import discord
from discord.ext import commands

class server_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="reset", help="Reset Server")
    async def r(self, ctx):
       pass