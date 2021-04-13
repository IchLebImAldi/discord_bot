import config

import discord
from discord.ext import commands

import os

#import all of the cogs

from music_cog import music_cog
from chat_cog import chat_cog
from server_cog import server_cog
from info_cog import info_cog
from roles_cog import roles_cog

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot

bot.add_cog(music_cog(bot))
bot.add_cog(chat_cog(bot))
bot.add_cog(server_cog(bot))
bot.add_cog(info_cog(bot))
bot.add_cog(roles_cog(bot))

#start the bot with our token
bot.run(config.token)