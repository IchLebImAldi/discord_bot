import config

import discord
from discord.ext import commands
import youtube_dl
import os


TOKEN = config.token
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), help_command=None)



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
        title = "Help"
    )
    mbed.add_field(name="!start", value="Resets Entire Server (roles/channels)")
    mbed.add_field(name="!createvc <name> <category>", value="Creates Voice Channel")
    mbed.add_field(name="!deletevc <name>", value="Deletes Voice Channel")
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
async def play(ctx, url):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = ctx.author.voice.channel
    
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

client.run(TOKEN)