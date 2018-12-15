import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import platform
import colorsys
import random
import os
import time
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType







client = commands.Bot(command_prefix = '/', case_insensitive=False)

client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name= "Prefix: /"))
    print("The bot is online and connected with Discord!") 
    
    

@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)

async def warn(ctx, userName: discord.User, *, message:str):
    channel = discord.utils.get(client.get_all_channels(), name='logs')
    
    embed = discord.Embed(color = 0xB22222,
        
        title = "Warning",
        description = """ __**You has been warned!**__
        User warned:
        ``{0}``
        Moderator:
        ``{1}`` 
        Reason:
        ``{2}``""".format(userName, ctx.message.author, message)
        
)
    await client.send_message(userName, embed=embed)
 

    embed = discord.Embed(color = 0xB22222, title = "Warning")
    embed.add_field(name = "User Warned", value = "{0}".format(userName), inline=False)
    embed.add_field(name = "Moderator", value = "{0}".format(ctx.message.author), inline=False)
    embed.add_field(name = "Reason", value = "{0}".format(message), inline=False)
 
    await client.send_message(channel, embed=embed)
   
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)

async def announce(ctx, userName: discord.User, *, message:str):
    channel = discord.utils.get(client.get_all_channels(), name='announcements')
    
    embed = discord.Embed(
        
        title = "Succesful!",
        description = """ __**Announce has been successfully made!**__"""
        
)
    await client.delete_message(ctx.message)
    await client.send_message(userName, embed=embed)
 

    
    embed = discord.Embed(title = "New Announcement! Nové Oznámení!", color = 0xFFFF00)
    embed.add_field(name = "Announcement:", value = "{0}".format(message), inline=False)
    embed.add_field(name = "Announced by:", value = "{0}".format(ctx.message.author), inline=False)
        
    await client.send_message(channel, "@everyone", embed=embed)
    

@client.command()
async def modhelp():
    embed = discord.Embed(title = "Help Pro/For Mods", color = 0xDC143C)
    embed.add_field(name = "/warn", value = "Použití/Usage: /warn @user Reason",inline=False)
    embed.add_field(name = "/kick", value = "Použití/Usage: /kick @user Reason",inline=False)
    embed.add_field(name = "/ban", value = "Použití/Usage: /ban @user Reason",inline=False)
    embed.add_field(name = "/clear", value = "Použití/Usage: /clear 1-∞",inline=False)
    embed.add_field(name = "/announce", value = "Oznámí něco, Announce Something",inline=False)
    embed.set_footer(text = "Bota udělala N  E  L  A™#8429 Bot made by N  E  L  A™#8429")
    await client.say(embed=embed)

@client.command()
async def help():
    embed = discord.Embed(title = "Help", color = 0x4B0082)
    embed.add_field(name = "========", value = "=====================", inline=False)
    embed.add_field(name = "/modhelp", value = "Ukáže/Shows mod help", inline = False) #warn, kick, ban, unban, clear
    await client.say(embed=embed)
    
client.run(os.getenv("BOT_TOKEN"))
