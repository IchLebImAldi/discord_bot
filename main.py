import config

import discord
from discord.ext import commands, tasks
from discord.utils import get
import youtube_dl
import os
import random
import time


TOKEN = config.token
client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), help_command=None)


def get_category_by_name(guild, category_name):
    
    category = None
    for c in guild.categories:
        if c.name == category_name:
            category = c
            break
    return category

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def createvc(ctx, channelName, category):
    await ctx.channel.purge(limit=1)
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Success",
        description = f'Channel: {channelName} has been created!'
    )
    if ctx.author.guild_permissions.manage_channels:
        await guild.create_voice_channel(name=channelName, category=await guild.create_category(category))
        await ctx.send(embed=mbed)

@createvc.error
async def createvc_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a name and a category for the vc.")


@client.command()
async def deletevc(ctx, vc: discord.VoiceChannel):
    await ctx.channel.purge(limit=1)
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
    await ctx.channel.purge(limit=1)
    guild = ctx.guild
    mbed = discord.Embed(
        title = "Help"
    )
    mbed.add_field(name=".start", value="Resets Entire Server (roles/channels)")
    mbed.add_field(name=".createvc <name> <category>", value="Creates Voice Channel")
    mbed.add_field(name=".deletevc <name>", value="Deletes Voice Channel")
    mbed.add_field(name=".play", value="Starts Lil Peep Radio")
    mbed.add_field(name=".pause", value="Pauses Radio")
    mbed.add_field(name=".resume", value="Resumes Radio")
    mbed.add_field(name=".stop", value="Stops Radio")
    mbed.add_field(name=".skip", value="Skips current Song")
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)


@client.command()
# will delete everything on the server and generate all necessary roles / channels / categories 
async def start(ctx):
    
    guild = ctx.guild
    author = ctx.author
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
        
        #delete all roles except Admin / everyone / Bot
        for role in guild.roles:
            if not (role.name == 'Admin' or role.name == '@everyone' or role.name == 'Bot'):
                await role.delete()

          
        
        role = await guild.create_role(name="BEANS", colour=discord.Colour(0x0000FF))

@client.command()
async def play(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = get(client.voice_clients, guild=ctx.guild)
  
    def repeat(guild, voice, audio):
        song = random.choice(os.listdir("D:\\Documents\\dev\Python\\discord_bot\\peep_songs")) 
        print(song)        
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("peep_songs/"+ song), after=lambda e: repeat(guild, voice, audio))
        voice.is_playing()
        

    if channel and not voice.is_playing():
        audio = discord.FFmpegPCMAudio('audio.mp3')
        voice.play(audio, after=lambda e: repeat(ctx.guild, voice, audio))
        voice.is_playing()
    
@client.command()
async def playStr(ctx, name):
    result = []

# Wlaking top-down from the root
    for root, dir, files in os.walk("D:\\Documents\\dev\Python\\discord_bot\\peep_songs"):
        for file in files:
            if name in file:
                print("yess")
                result.append(os.path.join(root, name))

    print(result)

@client.command()
async def pause(ctx):
    await ctx.channel.purge(limit=1)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    await ctx.channel.purge(limit=1)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def skip(ctx):
    await ctx.channel.purge(limit=1)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def stop(ctx):
    await ctx.channel.purge(limit=1)
    for x in client.voice_clients:
        if(x.guild == ctx.message.guild):
            return await x.disconnect()

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop(ctx.guild)


@client.command()
async def join(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

client.run(TOKEN)

