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
    
    
    embed = discord.Embed(color = 0xB22222, title = "User warned")
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
 

    
    embed = discord.Embed(title = "New Announcement!", color = 0xFFFF00)
    embed.add_field(name = "Announcement:", value = "{0}".format(message), inline=False)
    embed.add_field(name = "Announced by:", value = "{0}".format(ctx.message.author), inline=False)
        
    await client.send_message(channel, "@everyone", embed=embed)
    
@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, number):
 
    if ctx.message.author.server_permissions.manage_messages:
         mgs = [] #Empty list to put all the messages in the log
         number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number+1):
        mgs.append(x)            
       
    try:
        await client.delete_messages(mgs)          
        await client.say(str(number)+' messages deleted')
     
    except discord.Forbidden:
        await client.say(embed=Forbidden)
        return
    except discord.HTTPException:
        await client.say('clear failed.')
        return         
   
 
    await client.delete_messages(mgs)
    
@client.command()
@commands.has_permissions(kick_members=True)
async def modhelp():
    embed = discord.Embed(title = "For Mods", color = 0xDC143C)
    embed.add_field(name = "/warn", value = "Usage: /warn @user Reason",inline=False)
    embed.add_field(name = "/kick", value = "Usage: /kick @user",inline=False)
    embed.add_field(name = "/ban", value = "Usage: /ban @user ",inline=False)
    embed.add_field(name = "/clear", value = "Usage: /clear 1-∞",inline=False)
    embed.add_field(name = "/announce", value = "Announce Something",inline=False)
    embed.set_footer(text = "Bota udělala/Bot made by N  E  L  A™#8429")
    await client.say(embed=embed)

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def kick(ctx,user:discord.Member):
    channel = discord.utils.get(client.get_all_channels(), name='logs')
    embed = discord.Embed(title = "Kick", color = 0xFF4500)
    embed.add_field(name = "Moderator", value = "{0}".format(ctx.message.author), inline=False)
    embed.add_field(name = "User", value= "{0}".format(user), inline=False)
    

    if user.server_permissions.kick_members:
        await client.say('**He is mod/admin and i am unable to kick him/her!**')
        return
    
    try:
        await client.kick(user)
        await client.send_message(channel, embed=embed)
        await client.delete_message(ctx.message)

    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    
@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)      
async def ban(ctx,user:discord.Member):
    channel = discord.utils.get(client.get_all_channels(), name='logs')
    embed = discord.Embed(title = "Ban", color = 0xFF4500)
    embed.add_field(name = "Moderator", value = "{0}".format(ctx.message.author), inline=False)
    embed.add_field(name = "User", value = "{0}".format(user), inline=False)
    
    if user.server_permissions.ban_members:
        await client.say('**He is mod/admin and i am unable to ban him/her!**')
        return

    try:
        await client.ban(user)
        await client.send_message(channel, embed=embed)

    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return	
    
@client.command()
async def help():
    embed = discord.Embed(title = "Help", color = 0x4B0082)
    embed.add_field(name = "/ghelp", value = "Shows general help", inline=False)
    embed.add_field(name = "/modhelp", value = "Shows mod help", inline = False) #warn, kick, ban, unban, clear
    await client.say(embed=embed)
    
@client.command()
async def ghelp():
    embed = discord.Embed(title = "General help for everyone!", color = 0x66CC33)
    embed.add_field(name = "/userinfo", value = "Shows info about user!", inline=True)
    embed.add_field(name = "/info", value = "Shows info about this server!", inlinr=True)
    embed.set_footer(text = "Help summoned by {0}".format(ctx.message.author))
    await client.say(embed=embed)
    
client.run(os.getenv("BOT_TOKEN"))
