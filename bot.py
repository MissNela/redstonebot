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
    
    




@client.command()
async def help():
    embed = discord.Embed(title = "Help", color = 0x4B0082)
    embed.add_field(name = "========", value = "=====================", inline=False)
    embed.add_field(name = "/modhelp", value = "Ukáže/Shows mod help", inline = False) #warn, kick, ban, unban, clear
    await client.say(embed=embed)
    
client.run(os.getenv("BOR_TOKEN"))
