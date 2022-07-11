import discord
import asyncio
import random
import json
import os
import re
import logging
from discord import guild
from discord import Guild
from discord import Member
from discord import Intents
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops
from io import BytesIO
from datetime import datetime
from datetime import timedelta, timezone
from discord import colour, Spotify
from discord.embeds import Embed, EmbedProxy
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

TOKEN = None
client = commands.Bot(command_prefix = commands.when_mentioned_or('+'), case_insensitive=True, intents=Intents.all())
slash = SlashCommand(client, sync_commands=True)

prefix = '+'
guild_ids = [994631881918251028]

@client.event
async def on_ready():
    DiscordComponents(client)
    print(f'{client.user} ist jetzt online und startklar!')
    client.loop.create_task(status_task())
    

async def status_task():
    while True:
        mainserver = client.get_guild(994631881918251028)
        channel = client.get_channel(994636981512458350)
        await channel.edit(name=f'♤・{mainserver.member_count}')
        await client.change_presence(activity=discord.Game('+help | Metropole'), status=discord.Status.online)
        await asyncio.sleep(15)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{mainserver.member_count} Usern"))
        await asyncio.sleep(15)
        await client.change_presence(activity=discord.Game('Developed by Emi.'), status=discord.Status.online)
        await asyncio.sleep(15)


def is_not_pinned(mess):
    return not mess.pinned


def check_team(ctx):
    return client.get_guild(994631881918251028).get_role(994636091401449533) in ctx.author.roles


with open('./Neverland/blacklist.txt') as file:
    file = file.read().split()
@client.event
async def on_message(message):
    if message.author.bot:
        return
    #for badword in file:
    #    if badword in message.content:
    #        if message.author.guild_permissions.manage_messages():
    #            await message.delete()
    #            await message.channel.send(f'**{message.author.mention} bitte achte auf deine Wortwahl!**')
    if message.channel.id == 862732355088810036:
        if not message.attachments:
            await message.delete()
            try:
                await message.author.send(f"{message.author.mention} please only send pictures in this channel!")
            except:
                await message.author.send(f"{message.author.mention} please only send pictures in this channel!", delete_after=5)
    await client.process_commands(message)
    

@client.command(name='lock')
async def lock(ctx, channel: discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_messages:
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> Locked down - **{ctx.channel.name}**', color=0xE31316)
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> Locked down - **{channel.name}**', color=0xE31316)
            await channel.send(embed=embed)
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **manage messages**", color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='unlock')
async def unlock(ctx, channel: discord.TextChannel=None):
    if ctx.author.guild_permissions.manage_messages:
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=None)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> Unlocked - **{ctx.channel.name}**', color=0xE31316)
            await ctx.send(embed=embed)
        else:
            await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=None)
            embed = discord.Embed(title='Lockdown', description=f'<:JC_check:826282165423046666> Unlocked - **{channel.name}**', color=0xE31316)
            await channel.send(embed=embed)
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **manage messages**", color=0xff0000)
        await ctx.send(embed=embed)

#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        embed = discord.Embed(title='**An error has occurred.**', description=f'**Dieser Befehl (`{ctx.message.content}`) wurde nicht gefunden. Bitte überprüfe deine Rechtschreibung und versuche es erneut.**', color=0xff0000)
#        embed.set_footer(text='Für eine Liste aller Befehle, führe bitte den Befehl +help aus.')
#        await ctx.send(embed=embed)


#@client.command(name='help')
#async def help(ctx):
#    dev = client.get_user(515602740500627477)
#    prefix = ...
#    embed = discord.Embed(title='Helpdesk', description='Mein Prefix  ist `+`.', color=ctx.guild.me.color)
#    embed.add_field(name='Main Commands', value="`+help` - **Zeigt den Hilfebereich an.**\r\n"
#                                                "`+ping` - **Zeigt den Ping des Bots an.**", inline=False)
#    embed.add_field(name='Managment Commands', value="`+slowmode` - **Ändert den Slowmode eines Channels.**\r\n"
#                                                     "`+clear` - **Löscht eine angegebene anzahl von Nachrichten.**", inline=False)
#    embed.add_field(name='Moderation Commands', value="`+jail` - **Steckt einen Nutzer in den Knast.**\r\n"
#                                                      "`+unjail` - **Holt einen Nutzer aus dem Knast.**", inline=False)
#    embed.add_field(name='Fun Commands', value="`+say` - **Wiederholt alles nach dem Prefix.**\r\n"
#                                               "`+avatar` - **Zeigt den Avatar eines Users an.**\r\n"
#                                               "`+userinfo` - **Zeigt die Userinfo eines Users an.**\r\n"
#                                               "`+penis` - **Zeigt deine echte Penislänge an.**", inline=False)
#    embed.add_field(name="Custom-Commands", value="`+w` - **Begrüße ein neues Mitglied.**\r\n"
#                                                  "`+kiss` - **Küsse jemanden.**\r\n"
#                                                  "`+hug` - **Umarme jemanden.**\r\n"
#                                                  "`+slap` - **Klatsche jemanden.**\r\n"
#                                                  "`+kill` - **Töte jemanden.**\r\n"
#                                                  "`+gm` - **Wünsche allen einen guten Morgen.**\r\n"
#                                                  "`+gn` - **Wünsche allen eine gute Nacht.**", inline=False)
#    embed.set_footer(text='Bot by: ' + dev.name + '#' + dev.discriminator, icon_url=dev.avatar_url)
#    await ctx.send(embed=embed)


#@client.command()
#async def senddm(ctx):
#    if ctx.author.guild_permissions.administrator:
#        user = client.get_user(849744353165312010)
#        #user = random.choice(ctx.guild.members)
#        admins = [515602740500627477, 849744353165312010, 792839933387472918, 266305169573019659]
#        adminuser = client.get_user(random.choice(admins))
#        embed = discord.Embed(title='$9.99 Discord Nitro', description='[https://discord.gift/8h8weLD7s42lS](https://discord.gg/3DB85UGkj8)', color=0x2F3136)
#        embed.set_image(url='https://cdn.discordapp.com/attachments/862731059316391976/867887879106330654/image0.png')
#        await user.send(f'Hey {user.mention}, **Bibi<3#3015** has sent you a **$10 Discord Nitro** gift. Click the link to accept you nitro!', embed=embed)
#        await ctx.message.delete()


@client.command(name='say')
async def say(ctx, *, message):
    if '@everyone' in message:
        await ctx.send("Don't even think about mentioning `@ everyone`.")
    elif '@here' in message:
        await ctx.send("Don't even think about mentioning `@ here`.")
    else:
        await ctx.send(message)
        await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    global prefix
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**An error has occurred.**', description='**An important argument is missing.**', color=0xff0000)
        embed.add_field(name='Usage', value=f'`{prefix}say <message>`')
        await ctx.send(embed=embed)


@client.command(name='reminder')
async def reminder(ctx, time: int, *, reminder: str):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.send(f'**I will remind you in `{time}` seconds:** {reminder}')
        await asyncio.sleep(time)
        embed = discord.Embed(title='Erinnerung', description=reminder, timestamp=ctx.message.created_at, color=ctx.guild.me.color)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text='Reminder created at')
        await ctx.send(f"{ctx.author.mention}", embed=embed)


@client.command(name='editembed')
async def editembed(ctx, msg: discord.Message, hex, *, message):
    red = discord.Color.red()
    green = discord.Color.green()
    yellow = discord.Colour.orange()
    orange = discord.Colour.dark_orange()
    black = discord.Colour.dark_theme()
    white = discord.Color.light_gray()
    blue = discord.Colour.blue()
    darkblue = discord.Colour.dark_blue()
    darkgreen = discord.Colour.dark_green()
    purple = discord.Colour.purple()
    darkpurple = discord.Colour.dark_purple()
    blurple = discord.Colour.blurple()
    if hex == 'red':
        embed = discord.Embed(description=message, color=red)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'green':
        embed = discord.Embed(description=message, color=green)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'yellow':
        embed = discord.Embed(description=message, color=yellow)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'orange':
        embed = discord.Embed(description=message, color=orange)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'black':
        embed = discord.Embed(description=message, color=black)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'white':
        embed = discord.Embed(description=message, color=white)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'blue':
        embed = discord.Embed(description=message, color=blue)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'darkblue':
        embed = discord.Embed(description=message, color=darkblue)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'darkgreen':
        embed = discord.Embed(description=message, color=darkgreen)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'purple':
        embed = discord.Embed(description=message, color=purple)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'darkpurple':
        embed = discord.Embed(description=message, color=darkpurple)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'blurple':
        embed = discord.Embed(description=message, color=blurple)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'invisible':
        embed = discord.Embed(description=message, color=0x2F3136)
        await msg.edit(embed=embed)
        await ctx.message.delete()
    if hex == 'role' or hex == 'main':
        embed = discord.Embed(description=message, color=ctx.guild.me.color)
        await msg.edit(embed=embed)
        await ctx.message.delete()

@client.command(name='sendembed')
async def sendembed(ctx, hex, *, message):
    red = discord.Color.red()
    green = discord.Color.green()
    yellow = discord.Colour.orange()
    orange = discord.Colour.dark_orange()
    black = discord.Colour.dark_theme()
    white = discord.Color.light_gray()
    blue = discord.Colour.blue()
    darkblue = discord.Colour.dark_blue()
    darkgreen = discord.Colour.dark_green()
    purple = discord.Colour.purple()
    darkpurple = discord.Colour.dark_purple()
    blurple = discord.Colour.blurple()
    if hex == 'red':
        embed = discord.Embed(description=message, color=red)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'green':
        embed = discord.Embed(description=message, color=green)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'yellow':
        embed = discord.Embed(description=message, color=yellow)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'orange':
        embed = discord.Embed(description=message, color=orange)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'black':
        embed = discord.Embed(description=message, color=black)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'white':
        embed = discord.Embed(description=message, color=white)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'blue':
        embed = discord.Embed(description=message, color=blue)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'darkblue':
        embed = discord.Embed(description=message, color=darkblue)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'darkgreen':
        embed = discord.Embed(description=message, color=darkgreen)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'purple':
        embed = discord.Embed(description=message, color=purple)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'darkpurple':
        embed = discord.Embed(description=message, color=darkpurple)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'blurple':
        embed = discord.Embed(description=message, color=blurple)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'invisible':
        embed = discord.Embed(description=message, color=0x2F3136)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if hex == 'role' or hex == 'main':
        embed = discord.Embed(description=message, color=ctx.guild.me.color)
        await ctx.send(embed=embed)
        await ctx.message.delete()



@client.command(name='selfnick', hidden=True)
async def selfnick(ctx, *, newnick=None):
    if not newnick == None:
        username = client.get_guild(ctx.guild.id).get_member(client.user.id)
        await username.edit(nick=newnick)
        embed = discord.Embed(title="Nichname", description=f"I successfully changed my nickname to **{newnick}**.", color=ctx.guild.me.color)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        username = client.get_guild(ctx.guild.id).get_member(client.user.id)
        await username.edit(nick=None)
        embed = discord.Embed(title="Nichname", description=f"I successfully reset my nickname.", color=ctx.guild.me.color)
        await ctx.send(embed=embed)
        await ctx.message.delete()



@client.command(name='role')
async def role(ctx, member: discord.Member, role: discord.Role, time: int=None):
    if ctx.author.guild_permissions.manage_messages:
        if role in ctx.guild.roles:
            if ctx.author.top_role.position-1 >= role.position:
                botrole = ctx.guild.me
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(description=f'`✅` {role.mention} has been removed from {member.mention}.', color=ctx.guild.me.color)
                    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    if time != None:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'`✅` {role.mention} was added to {member.mention} for ** {time} s **.', color=ctx.guild.me.color)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(time)
                        await member.remove_roles(role)
                    else:
                        await member.add_roles(role)
                        embed = discord.Embed(description=f'`✅` {role.mention} was added to {member.mention}.', color=ctx.guild.me.color)
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'`❌` This role is too powerful to manage.\r\nPlease ask a senior team member or the owner for help.', color=0xff0000)
                embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=embed)

@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(description=f'`❌` The expected role was not found.', color=0xff0000)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)



@client.command(name='logout', hidden=True)
async def logout(ctx):
    if(ctx.author.id == 515602740500627477):
        embed = discord.Embed(description='**Bot logging out...**', color=0xff0000)
        await ctx.send(embed=embed)
        await client.logout()


@client.command(name='ping')
async def ping(ctx):
    await ctx.send('**Pong!** :ping_pong: __**{0}s**__'.format(round(client.latency, 3)))


@client.command(name='avatar', aliases=['av'])
@commands.cooldown(1, 10, type=BucketType.user)
async def avatar(ctx, user: discord.User):
    if user != None:
        embed = discord.Embed(title='Avatar', color=ctx.guild.me.color)
        embed.set_image(url=user.avatar_url)
        embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Avatar', color=ctx.guild.me.color)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.name + '#' + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@avatar.error
async def avatar_self(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"chill bro!",description=f"You're going too fast!\r\nTry again in **{error.retry_after:.0f}s**.", color=0xff0000)#{error.retry_after:.2f}s
        await ctx.send(embed=em)

@client.command(name='userinfo', aliases=['whois'])
@commands.cooldown(1, 10, type=BucketType.user)
async def userinfo(ctx, user: discord.User):
    highrole = user.top_role.mention
    highrolecolor = user.top_role.color
    if highrole == "@everyone":
        highrole = "None"
    if user != None:
        em = discord.Embed(description='**React with 🗑️ to delete the user info again.**', colour=highrolecolor)
        em.add_field(name='Nickname', value=user.nick, inline=True)
        em.add_field(name='Status', value=user.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=user.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{user.avatar_url}')
        em.set_author(name=user, icon_url=f'{user.avatar_url}')
        em.set_footer(text=f'User ID: {user.id}')
        msg = await ctx.send(embed=em)
        await msg.add_reaction('🗑️')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🗑️'
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
        else:
            await msg.delete()
            await ctx.message.delete()
    else:
        em = discord.Embed(description='**React with 🗑️ to delete the user info again.**', colour=highrolecolor)
        em.add_field(name='Nickname', value=ctx.author.nick, inline=True)
        em.add_field(name='Status', value=ctx.author.status, inline=True)
        em.add_field(name='Aktivität/Custom-Stauts', value=ctx.author.activity, inline=True)
        em.add_field(name='Höchste Rolle', value=highrole, inline=True)
        em.add_field(name='Account erstellt', value=ctx.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.add_field(name='Server beigetreten', value=ctx.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=f'{ctx.author.avatar_url}')
        em.set_author(name=ctx.author, icon_url=f'{ctx.author.avatar_url}')
        em.set_footer(text=f'User ID: {ctx.author.id}')
        msg = await ctx.send(embed=em)
        await msg.add_reaction('🗑️')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🗑️'
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
        else:
            await msg.delete()
            await ctx.message.delete()

@userinfo.error
async def userinfo_self(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"chill bro!",description=f"You're going too fast!\r\nTry again in **{error.retry_after:.0f}s**.", color=0xff0000)#{error.retry_after:.2f}s
        await ctx.send(embed=em)


@client.command(name='addreaction', aliases=['react'])
async def addreaction(ctx, msgid: int, emoji: str):
    if ctx.author.guild_permissions.manage_messages:
        msg = await ctx.fetch_message(msgid)
        if msg:
            await msg.add_reaction(emoji)
            await ctx.message.add_reaction('✅')


@client.command(name='slowmode')
async def slowmode(ctx):
    if ctx.author.guild_permissions.manage_messages:
        args = ctx.message.content.split(' ')
        if len(args) == 2:
            if args[1].isdigit():
                zahl = int(args[1])
                await ctx.channel.edit(slowmode_delay=zahl)
                embed = discord.Embed(description=f':alarm_clock: The slow mode of this channel was updated to **{args [1]} seconds**!', color=ctx.guild.me.color)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
        else:
            embed = discord.Embed(description='`❌` Please enter a time to which the slow mode should be set!\r\n'
                                              '\r\n'
                                              '__Usage:__ `+slowmode <number>`', color=0xff0000)
            await ctx.send(embed=embed)
            await ctx.message.delete()
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **manage messages**", color=0xff0000)
        await ctx.send(embed=embed)
        await ctx.message.delete()


@client.command(name='clear')
async def clear(ctx):
    if ctx.author.guild_permissions.manage_messages:
        args = ctx.message.content.split(' ')
        if len(args) == 2:
            if args[1].isdigit():
                count = int(args[1]) + 1
                deleted = await ctx.channel.purge(limit=count, check=is_not_pinned)
                embed = discord.Embed(description=':wastebasket: **{}** Messages deleted.'.format(len(deleted)-1), color=ctx.guild.me.color)
                await ctx.send(embed=embed, delete_after=3)
        else:
            embed = discord.Embed(description='`❌` Please enter a valid number of messages to be deleted.\r\n'
                                              '\r\n'
                                              '__Usage:__ `+clear <number>`', color=0xff0000)
            await ctx.send(embed=embed, delete_after=10)
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **manage messages**", color=0xff0000)
        await ctx.send(embed=embed, delete_after=10)


@client.command(name='penis')
@commands.cooldown(1, 10, type=BucketType.user)
async def penis(ctx, user: discord.User):
    embed = discord.Embed(title="Stop stop... wait a minute...", description="You can only see your own penis length. (Unless someone allows you to look inside their pants :eyes:)", color=0xff0000)
    await ctx.send(embed=embed)
# Du kannst nur deine eigene Penislänge einsehen. (Außer jemand erlaubt es dir in seine Hose zu sehen :eyes:)

@penis.error
async def penis_self(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        color = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
                  discord.Colour.blue(), discord.Colour.purple(), discord.Colour.magenta()]
        penis = ['', '=', '==', '===', '====', '=====', '======', '=======', '========', '=========', '==========', '===========', '============', '=============', '==============', '===============', '================']
        embed = discord.Embed(title="Penis", description=f"{ctx.author.name}'s Penis\r\n"
                                                              "8" + random.choice(penis) + "D", color=ctx.guild.me.color)
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"chill bro!",description=f"You're going too fast!\r\nTry again in **{error.retry_after:.0f}s**.", color=0xff0000)#{error.retry_after:.2f}s
        await ctx.send(embed=em)


@client.command(name='setupmute')
async def setupmute(ctx):
    if ctx.author.guild_permissions.administrator:
        for allchannels in ctx.guild.text_channels:
            role = client.get_guild(994631881918251028).get_role(862751357127229450)
            await allchannels.set_permissions(role, send_messages=False, add_reactions=False)
        for allchannels in ctx.guild.voice_channels:
            role = client.get_guild(994631881918251028).get_role(862751357127229450)
            await allchannels.set_permissions(role, speak=False)
        await ctx.send('Vorgang abgeschlossen.')


@client.command(name='mute')
async def mute(ctx, user: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if not user == ctx.author:
            role = discord.utils.get(ctx.guild.roles, id=862751357127229450)
            await user.add_roles(role, reason=reason)
            embed = discord.Embed(description=f'{user.mention}: {user.id} was muted successfully!', color=ctx.guild.me.color)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            dmembed = discord.Embed(description=f'{user.mention} you were muted on the {ctx.guild.name} server!', color=ctx.guild.me.color)
            dmembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            if reason == None:
                embed.add_field(name='Reason:', value='No reason given.')
                dmembed.add_field(name='Reason:', value='No reason given.')
            else:
                embed.add_field(name='Reason:', value=reason)
                dmembed.add_field(name='Reason:', value=reason)
            await ctx.send(embed=embed)
            try:
                await user.send(embed=dmembed)
            except:
                pass
        else:
            embed = discord.Embed(description="`❌` I'm sorry, but you can't mute yourself.", color=0xff0000)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **kick members**", color=0xff0000)
        await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**An error has occurred.**', description='**Please mention a user.**', color=0xff0000)
        await ctx.send(embed=embed)


@client.command(name='unmute')
async def unmute(ctx, user: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        role = discord.utils.get(ctx.guild.roles, id=862751357127229450)
        await user.remove_roles(role, reason=reason)
        embed = discord.Embed(description=f'{user.mention}:{user.id} was unmuted successfully!', color=ctx.guild.me.color)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        dmembed = discord.Embed(description=f'{user.mention} your mute on the {ctx.guild.name} server was revoked!', color=ctx.guild.me.color)
        dmembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        try:
            await user.send(embed=dmembed)
        except:
            pass
    else:
        embed = discord.Embed(description="`❌` I'm sorry, but you are not allowed to use this command!\r\n"
                                          "\r\n"
                                          "__Missing permission:__ **kick members**", color=0xff0000)
        await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='**An error has occurred.**', description='**Please mention a user.**', color=0xff0000)
        await ctx.send(embed=embed)


players = {}

@client.command()
async def connect(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()


### Ticket-System
@client.command(name='ticketembed')
async def ticketembed(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(description=message, color=ctx.guild.me.color)
        embed.set_author(name='🎫 Ticket Support')
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()
        await msg.add_reaction('🎫')


@client.command(pass_context=True)
async def ticket(ctx, cmd):
    with open("./ChillHood/ch_tickets.json") as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
        logchannel = client.get_channel(863036873873424394)
        teamrole = client.get_guild(994631881918251028).get_role(863037151814090791)
        if cmd == 'claim':
            if teamrole in ctx.author.roles:
                embed = discord.Embed(description=f'{ctx.author.mention} will take care of you now.', color=discord.Color.gold())
                ticket_number = int(data["ticket-counter"])
                await ctx.channel.edit(name=f'claimed-{ticket_number}')
                msg = await ctx.channel.send(embed=embed)
                await ctx.message.delete()
                logembed = discord.Embed(title='Log - Ticket claimed', description=f'The ticket **#{ctx.channel.name}** ({ctx.channel.mention}) was claimed by **{ctx.author}**.', color=discord.Colour.gold())
                await logchannel.send(embed=logembed)
        if cmd == 'close':
            embed = discord.Embed(description=':lock: The ticket was closed.\r\n'
                                              '`+ticket delete` to delete the ticket.', color=discord.Color.orange())
            ticket_number = int(data["ticket-counter"])
            clsoverwrites = None
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                        send_messages=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            await ctx.channel.edit(overwrites=clsoverwrites)
            await ctx.channel.edit(overwrites=overwrites)
            await ctx.channel.edit(name=f'closed-{ticket_number}')
            msg = await ctx.channel.send(embed=embed)
            await ctx.message.delete()
            logembed = discord.Embed(title='Log - Ticket closed', description=f'The ticket **#{ctx.channel.name}** ({ctx.channel.mention}) was closed by **{ctx.author.name}**.', color=discord.Colour.orange())
            msg = await logchannel.send(embed=logembed)
        if cmd == 'delete':
            if teamrole in ctx.author.roles:
                embed2 = discord.Embed(description='**Dieses Ticket wird in `5` Sekunden gelöscht...**', color=0xff0000)
                await ctx.send(embed=embed2)
                await asyncio.sleep(5)
                logembed = discord.Embed(title='Log - Ticket deleted', description=f'The ticket **#{ctx.channel.name}** was deleted by **{ctx.author.name}**.', color=discord.Colour.red())
                msg = await logchannel.send(embed=logembed)
                data["ticket-channel-ids"].remove(ctx.channel.id)
                await ctx.channel.delete()

@client.command()
async def s(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("couldn't find a message to snipe")
        return

    embed = discord.Embed(description=contents, color=discord.Color.dark_gold(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)
    
    
@client.event
async def on_raw_reaction_add(reaction):
    user = reaction.member
    server = client.get_guild(reaction.guild_id)
    if reaction.message_id == 863036833508098099:
        if reaction.emoji == discord.PartialEmoji(name="🎫"):
            logchannel = client.get_channel(863036873873424394)
            msgid = reaction.message_id
            ticketchannel = client.get_channel(862733245664854036)
            ticketmessage = await ticketchannel.fetch_message(msgid)
            await ticketmessage.remove_reaction(discord.PartialEmoji(name="🎫"), user)
            with open("./ChillHood/ch_tickets.json") as f:
                data = json.load(f)
            teamrole = client.get_guild(994631881918251028).get_role(994636091401449533)
            ticketrole = client.get_guild(994631881918251028).get_role(863037151814090791)
            overwrites = {
                server.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                        send_messages=True),
                user: discord.PermissionOverwrite(read_messages=True),
                teamrole: discord.PermissionOverwrite(read_messages=True),
                server.me: discord.PermissionOverwrite(read_messages=True)
            }
            ticketcat = client.get_channel(862733214450450432)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            data["ticket-counter"] = int(ticket_number)
            channel = await server.create_text_channel(f"ticket-{ticket_number}", category=ticketcat, overwrites=overwrites)
            data["ticket-channel-ids"].append(channel.id)
            with open("./ChillHood/ch_tickets.json", 'w') as f:
                json.dump(data, f)
            await ticketchannel.send(f'Dein Ticket **#{ticket_number}** wurde erstellt. - {channel.mention}', delete_after=5)
            embed = discord.Embed(title='Support-Ticket', description='Welcome to your ticket.\r\n'
                                                                      'Please tell us your request in as much detail as possible. \r\n'
                                                                      f'A {ticketrole.mention} will take care of you shortly.', color=discord.Colour.green())
            embed.add_field(name='Use the following commands to add members to the ticket or to close the ticket:', value= '➩ `+ticket adduser <user>`\r\n➩ `+ticket close`', inline=False)
            msg = await channel.send(f'Hello {user.mention}.', embed=embed)
            logembed = discord.Embed(title='Log - Ticket opened', description=f'**{user}** opened a ticket. The ticket channel is {channel.mention}.', color=discord.Colour.dark_green())
            msg = await logchannel.send(ticketrole.mention, embed=logembed)
### Tickt-System Ende
    elif reaction.message_id == 863041288706326579:
        if reaction.emoji == discord.PartialEmoji(name="✅"):
            user = reaction.member
            role = client.get_guild(994631881918251028).get_role(862722406979731516)
            msg = await client.get_channel(862738026060316692).fetch_message(reaction.message_id)
            await user.add_roles(role)
            await msg.remove_reaction(reaction.emoji, user)


@client.command()
async def vc(ctx, cmd, *, value=None):
    voicec = ctx.author.voice
    if cmd == 'cleanup':
        if ctx.author.guild_permissions.manage_messages:
            count = 0
            embed = discord.Embed(title='**Custom Voice**', description='<a:ch_clock:862740071195213854> **Clearing up...**', color=ctx.guild.me.color)
            msg = await ctx.send(embed=embed)
            for emptychannels in ctx.guild.voice_channels:
                if emptychannels.category.id == 850113571215900677:
                    if len(emptychannels.members) == 0:
                        if emptychannels.id != 850113572373266444:
                            await emptychannels.delete()
                            count += 1
            embed2 = discord.Embed(title='**Custom Voice**', description=f'`✅` **Cleanup complete.**\r\n\r\nDeleted channels: `{str(count)}`', color=ctx.guild.me.color)
            await msg.edit(embed=embed2)
    elif voicec:
        channel = voicec.channel
        if channel.category_id == 862733571151626320:
            if channel.permissions_for(ctx.author).manage_channels:
                if cmd == 'lock':
                    await channel.set_permissions(ctx.guild.default_role, connect=False)
                    embed = discord.Embed(title='**Custom Voice**', description='`✅` **Your channel was closed**', color=ctx.guild.me.color)
                    await ctx.send(embed=embed)

                elif cmd == 'unlock':
                    await channel.set_permissions(ctx.guild.default_role, connect=None)
                    embed = discord.Embed(title='**Custom Voice**', description='`✅` **Your channel was opened**', color=ctx.guild.me.color)
                    await ctx.send(embed=embed)
                elif cmd == 'hide':
                    await channel.set_permissions(ctx.guild.default_role, view_channel=False)
                    embed = discord.Embed(title='**Custom Voice**', description='`✅` **Your channel is now hidden**', color=ctx.guild.me.color)
                    await ctx.send(embed=embed)
                elif cmd == 'unhide':
                    await channel.set_permissions(ctx.guild.default_role, view_channel=None)
                    embed = discord.Embed(title='**Custom Voice**', description='`✅` **Your channel is now visible**', color=ctx.guild.me.color)
                    await ctx.send(embed=embed)
                elif cmd == 'rename':
                    if value != None:
                        oldname = channel.name
                        await channel.edit(name=str(value))
                        embed = discord.Embed(title='**Custom Voice**', description=f'`✅` **Der Name deines Kanals wurde auf _{value}_ aktualisiert**', color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe den neuen Namen an.**', color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                elif cmd == 'limit':
                    if value != None:
                        if value == '0':
                            await channel.edit(user_limit=None)
                            embed = discord.Embed(title='**Custom Voice**', description=f'`✅` **Das Userlimit deines Kanals wurde auf `{value}` aktualisiert.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                        elif int(value):
                            await channel.edit(user_limit=int(value))
                            embed = discord.Embed(title='**Custom Voice**', description=f'`✅` **Das Userlimit deines Kanals wurde auf `{value}` aktualisiert.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe das neue Limit an.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe das neue Limit an.**', color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                elif cmd == 'add':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            await channel.set_permissions(user, view_channel=True, connect=True, speak=True)
                            embed = discord.Embed(title='**Custom Voice**', description=f'`✅` {user.mention} **wurde zu deinem Kanal hinzugefügt.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe die ID eines Nutzers an.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe die ID eines Nutzers an.**', color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                elif cmd == 'remove':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            await channel.set_permissions(user, overwrite=None)
                            embed = discord.Embed(title='**Custom Voice**', description=f'`✅` {user.mention} **wurde aus deinem Kanal entfernt.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe die ID eines Nutzers an.**', color=ctx.guild.me.color)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte gebe die ID eines Nutzers an.**', color=ctx.guild.me.color)
                        await ctx.send(embed=embed)
                elif cmd == 'transfer':
                    if value != None:
                        if int(value):
                            user = client.get_user(int(value))
                            embed = discord.Embed(title='**Custom Voice**', description=f'Bist du sicher dass du den Kanal {channel.mention} an {user.mention} übertragen möchtest?', color=ctx.guild.me.color)
                            embed.set_footer(text='"Ja" zum Bestätigen')
                            msg = await ctx.send(embed=embed, components=[[Button(style=3, label="Ja"), Button(style=4, label="Nein")]])

                            def check(res):
                                return ctx.author == res.user and res.channel == ctx.channel

                            try:
                                res = await client.wait_for("button_click", check=check, timeout=30)
                                await res.respond(type=6)
                                if res.component.label == 'Ja':
                                    successembed = discord.Embed(title='**Custom Voice**', description=f'Der Kanal {channel.mention} wurde an {user.mention} übertragen.', color=discord.Colour.green())
                                    successembed.set_footer(text='Bestätigt')
                                    await channel.set_permissions(user, view_channel=True, connect=True, move_members=True, manage_channels=True,
                                                                        deafen_members=True, mute_members=True, speak=True)
                                    await channel.set_permissions(ctx.author, view_channel=True, connect=True, speak=True)
                                    await msg.edit(embed=successembed, components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
                                else:
                                    abbortembed = discord.Embed(title='**Custom Voice**', description=f'Die übertragung des Kanals {channel.mention} wurde wiederrufen.', color=discord.Colour.red())
                                    abbortembed.set_footer(text='Wiederrufen')
                                    await msg.edit(embed=abbortembed, components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
                            
                            except asyncio.TimeoutError:
                                await msg.edit(components=[[Button(style=3, label="Ja", disabled=True), Button(style=4, label="Nein", disabled=True)]])
            else:
                embed = discord.Embed(title='**Custom Voice**', description='`❌` **Du hast keine Berechtigungen für änderungen an diesem Kanal!**', color=ctx.guild.me.color)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**Custom Voice**', description='`❌` **Du hast keine Berechtigungen für änderungen an diesem Kanal!**', color=ctx.guild.me.color)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='**Custom Voice**', description='`❌` **Bitte tritt einem Custom Voice bei, bevor du diesen Befehl verwenden kannst.**', color=ctx.guild.me.color)
        await ctx.send(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        def voicecheck(x, y, z):
            return len(newchannel.members) == 0
        if after.channel.id == 862736488519958558:
            maincategory = client.get_channel(862733571151626320)
            newchannel = await member.guild.create_voice_channel(name=f'⏳ {member.name}', category=maincategory)
            await newchannel.set_permissions(member, connect=True, move_members=True, manage_channels=True,
                                            deafen_members=True, mute_members=True, speak=True)
            await member.move_to(newchannel)
            await client.wait_for('voice_state_update', check=voicecheck)
            await newchannel.delete()


@client.event
async def on_member_join(member):
    channel = client.get_channel(994631882362855514)
    await channel.send(f'Hey {member.mention}, welcome to **{member.guild.name}**! <a:mp_cheers:995716627528163349>')
    memberrole = client.get_guild(member.guild).get_role(994642978301808700)
    await member.add_roles(memberrole)


client.run(TOKEN)
