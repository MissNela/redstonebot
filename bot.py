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
    
def owner(ctx):
    return ctx.message.author.id == "342364288310312970"

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
@commands.check(owner)
async def restart():
    await client.logout()

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
    embed.add_field(name = "/updates", value = "Shows update (Owner only)", inline=False)
    embed.add_field(name = "/restart", value = "Restarts a bot! Owner Only", inline=False)
    embed.set_footer(text = "Bot made by N  E  L  A™#8429")
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
     

async def info(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);

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
    
@client.command(pass_context = True)
async def ghelp():
    embed = discord.Embed(title = "General help for everyone!", color = 0x66CC33)
    embed.add_field(name = "/userinfo", value = "Shows info about user!", inline=True)
    embed.add_field(name = "/info", value = "Shows info about this server!", inline=True)
   
    embed.set_footer(text = "Help made by Nela!")
    await client.say(embed=embed)
    
@client.command(pass_context=True)
async def ping(ctx):
    t = await client.say('Pong!')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content=':ping_pong: Pong! Actual ping: {}ms'.format(int(ms)))
    
@client.command(pass_context=True)
async def amiowner():
    if "Redstone Master" in [role.name for role in message.author.roles]:
        await client.say("YOU ARE AN OWNER! MA LORD!")
    else:
        await client.say("YOU ARE NOT MY OWNER GO FUCK URSELF!")
        
@client.command()
async def set_prefix(self, prefix):
    
    self.command_prefix = prefix
    await self.change_presence(game=discord.Game(name='{}help for help'.format(prefix)))
    
@client.command(pass_context = True)
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)
 
@client.command()

async def updates():
   
    embed = discord.Embed(title = "New Update!", color = 0x00BFFF)
    embed.add_field(name = "Userinfo", value = "We added ``/userinfo`` command to get info about user!",inline=False)
    embed.add_field(name = "info", value = "We added ``/info`` to get info about server!",inline=False)
    embed.add_field(name = "#Developer Commands#", value = " ",inline=False)
    embed.add_field(name = "restart", value = "Developer can restart bot with ``/restart`` cmd if needed.",inline=False)
    embed.add_field(name = "&Preparing&", value = "Preparing __**Redstone Bot Premium**__!!",inline=False)
    embed.set_footer(text = "Bot made by N  E  L  A#8429 | Redstone commands preparing!")
    await client.say(channel, embed=embed)

client.run(os.getenv("BOT_TOKEN"))
