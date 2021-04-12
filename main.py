import config

import discord
from discord.ext import commands
from discord.utils import get


TOKEN = config.token
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('!'), help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def createvc(ctx, channelName):
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Success",
        description = f'Channel: {channelName} has been created!'
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_voice_channel(name=channelName)
        await ctx.send(embed=mbed)

@client.command()
async def deletevc(ctx, vc: discord.VoiceChannel):
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Success",
        description = f'Channel: {vc} has been deleted!'
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await vc.delete()

@client.command()
async def help(ctx):
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Help",
        description = f'!createvc <name>:  Will create a Voicechannel'
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)


@client.command()
# will delete everything on the server and generate all necessary roles / channels / categories 
async def start(ctx):
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Success",
        description = 'Channels have been created!'
    )
    if ctx.author.guild_permissions.manage_channels:
        #delete all channels
        for c in guild.channels:
            await c.delete()
        
        #create all channels/categories needed
        text_category = await guild.create_category("📃Text")
        talk_category = await guild.create_category("🎤Talk")
        await guild.create_text_channel(name="⌨Chat", category=text_category)

        for i in  range(6)[1:]:
            await guild.create_voice_channel(name=f"Talk {i}", category=talk_category)
        


client.run(TOKEN)