import discord
from discord.ext import commands, tasks

class roles_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.loop.start()
        

    @tasks.loop(seconds=2)
    async def loop(self):
        pass#role = discord.utils.get(guild.roles, name="")


        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot started. Latency: {int(self.bot.latency*1000)}ms")

