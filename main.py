import config

import discord
from discord.ext import commands



TOKEN = config.token
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), help_command=None)


def get_member(discordname):
    for guild in client.guilds:
        for member in guild.members:
            if member.name == discordname:
                return member

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
            if (role.name == 'Admin' or role.name == '@everyone' or role.name == 'Bot') == False:
                await role.delete()

          
        
        role = await guild.create_role(name="BEANS", colour=discord.Colour(0x0000FF))

        


client.run(TOKEN)