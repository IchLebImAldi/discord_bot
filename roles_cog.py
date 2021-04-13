import discord
from discord.ext import commands, tasks

class roles_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop.start()
        

    @tasks.loop(seconds=2)
    async def loop(self):
        pass#role = discord.utils.get(member.server.roles, name="")


        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot started. Latency: {int(self.bot.latency*1000)}ms")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(831280507924381697).send(member)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_channel(831280507924381697).send(member)


    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)