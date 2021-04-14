import discord
from discord.ext import commands

class chat_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="clear", help="Clear chat")
    async def c(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)