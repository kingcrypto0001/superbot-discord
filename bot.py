import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import json
import time
import os

TOKEN = "MzkwMzI5NzE5ODcyMTU5NzY1.Dnxfsw.-IPj66ctnLzZnMrGTdUI8jZnGnU"
VERSION = "v0.08"
PREFIX = ">"
OWNERID = ["248242789169496064", "307934179738386452"] #ME, Astraqa

client = commands.Bot(command_prefix = PREFIX)
client.remove_command("help")


#ON READY EVENT
@client.event
async def on_ready():
    global SERVERS
    SERVERS = str(len(client.servers))
    global normal_status
    normal_status = VERSION + " | " + PREFIX + "help | Servers: " + SERVERS
    print(normal_status)
    await client.change_presence(game = discord.Game(name = normal_status))
    print("Bot Connected.")

#ON MESSAGE EVENT
@client.event
async def on_message(message):
    try:
        message.content = message.content.lower()
        await client.process_commands(message)
    except: discord.ext.commands.CommandNotFound


#CLEAR COMMAND
@client.command(pass_context = True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    amount = int(amount)
    messages = []
    async for message in client.logs_from(channel, limit = amount):
        if amount > 100:
            await client.delete_message(message)
            await asyncio.sleep(0.05)    
        elif amount <= 100:           
            messages.append(message)

    try:
        await client.delete_messages(messages)
    except:
        discord.errors.NotFound, discord.errors.ClientException, discord.ext.commands.errors.CommandInvokeError

#CHANGE STATUS COMMAND
@client.command(pass_context = True)
async def status(ctx, *args):
    for ownerid in OWNERID:
        if ctx.message.author.id == ownerid:
            output = ""
            for word in args:
                output = output + word
                output = output + " "

            if output == "(normal) ":
                await client.change_presence(game = discord.Game(name = normal_status))
                await client.say("Status was changed to " + normal_status)
            else:
                await client.change_presence(game = discord.Game(name = output))
                await client.say("Status was changed to " + output)
        else:
            try: 
                await client.delete_message(ctx.message)
            
            except: discord.errors.NotFound, discord.errors.ClientException, discord.ext.commands.errors.CommandInvokeError

#BITCOIN BOT COMMAND
@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        embed = discord.Embed(color = discord.Colour.blue())
        embed.set_author(name = "Bitcoin price is: $" + response["bpi"]["USD"]["rate"] + " | Last Updated: " + response["time"]["updated"])
        await client.say(embed = embed)

#ECHO BOT COMMAND
@client.command(pass_context = True)
async def echo(ctx, *args):
    await client.delete_message(ctx.message)
    output = ""
    for word in args:
        output = output + word
        output = output + " "

    embed = discord.Embed(
        colour = discord.Colour.blue()    
    )

    embed.set_author(name = output)
    
    await client.say(embed = embed)

#DM COMMAND
@client.command(pass_context = True)
async def dm(ctx, user : discord.Member, *args): # : discord.Member
    
        output = ""
        for word in args:
            output = output + word
            output = output + " "
        

        embed = discord.Embed(title = output, colour = discord.Colour.blue())

        await client.send_message(user, embed = embed)
        
#PING BOT COMMAND
@client.command(pass_context = True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title = "Ping: {}".format(round((t2-t1)*1000)), colour = discord.Colour.blue())
    await client.say(embed=embed) 

#RESTART BOT COMMAND
@client.command()
async def restart():
    await client.say("Restarting bot...")
    await client.close()
    await client.connect()
    await client.say("Restarted bot.")

#HELP COMMAND
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        title = "Prefix: " + PREFIX,
        colour = discord.Colour.blue()
    )

    embed.set_author(name = "HELP")
    
    embed.add_field(name = "clear", value = "Clears the amount of messages [arg1]. You can only delete more then 2 messages.", inline = False)
    embed.add_field(name = "bitcoin", value = "Shows 1 BTC amount in USD.", inline = False)

    await client.say(embed = embed)

#CMD ERROR EVENT
@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.DisabledCommand):
        return
    try:
        if isinstance(error.original, discord.Forbidden):
            return
        elif isinstance(error.original, discord.HTTPException) and 'empty message' in str(error.original):
            return
        elif isinstance(error.original, aiohttp.ClientOSError):
            return
    except AttributeError:
        pass

    if isinstance(error, commands.BadArgument):
        fmt = "Please provide a valid argument to pass to the command: {}".format(error)
        await client.send_message(ctx.message.channel, fmt)
    elif isinstance(error, commands.CheckFailure):
        fmt = "You can't tell me what to do!"
        await client.send_message(ctx.message.channel, fmt)
    elif isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        fmt = "This command is on cooldown! Hold your horses! >:c\nTry again in {} minutes and {} seconds" \
            .format(round(m), round(s))
        await client.send_message(ctx.message.channel, fmt)
    elif isinstance(error, commands.NoPrivateMessage):
        fmt = "This command cannot be used in a private message"
        await client.send_message(ctx.message.channel, fmt)
    elif isinstance(error, commands.MissingRequiredArgument):
        await client.send_message(ctx.message.channel, error)
    else:
        now = datetime.datetime.now()
        with open("error_log", 'a') as f:
            print("In server '{0.message.server}' at {1}\nFull command: `{0.message.content}`".format(ctx, str(now)),
                  file=f)
            try:
                traceback.print_tb(error.original.__traceback__, file=f)
                print('{0.__class__.__name__}: {0}'.format(error.original), file=f)
            except:
                traceback.print_tb(error.__traceback__, file=f)
                print('{0.__class__.__name__}: {0}'.format(error), file=f)








































#RUN BOT
client.run(TOKEN)
