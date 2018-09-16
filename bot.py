import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import json
import time
import os

TOKEN = "MzkwMzI5NzE5ODcyMTU5NzY1.Dnxfsw.-IPj66ctnLzZnMrGTdUI8jZnGnU"
VERSION = "v0.04"
PREFIX = ">"
OWNERID = "248242789169496064"

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

#CLEAR COMMAND
@client.command(pass_context = True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit = int(amount)):            
        messages.append(message)
    await client.delete_messages(messages)

#CHANGE STATUS COMMAND
@client.command(pass_context = True)
async def status(ctx, *args):
    if ctx.message.author.id == OWNERID:
        output = ""
        for word in args:
            output = output + word
            output = output + " "

        print(output)
        if output == "(normal) ":
            await client.change_presence(game = discord.Game(name = normal_status))
            await client.say("Status was changed to " + normal_status)
        else:
            await client.change_presence(game = discord.Game(name = output))
            await client.say("Status was changed to " + output + ".")
    else:
        await client.say("You don't have permission to run the command.")

#BITCOIN BOT COMMAND
@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response["bpi"]["USD"]["rate"] + " | Last Updated: " + response["time"]["updated"])

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

    embed.set_author(name = "*HELP*")
    
    embed.add_field(name = "clear", value = "Clears the amount of messages [arg1]", inline = False)
    embed.add_field(name = "bitcoin", value = "Shows 1 BTC amount in USD.", inline = False)

    await client.say(embed = embed)










































#RUN BOT
client.run(TOKEN)
