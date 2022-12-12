import discord

import json

from discord.ext import commands

import youtube_dl

client = commands.Bot(command_prefix='s!',intents=discord.Intents.all())

@client.event

async def on_ready():

    print(f"{client.user} has connected to discord!")
    await client.user.change_presence(status="Use s! for commands")

@client.command()

async def echo(ctx,*, message):

    await ctx.send(f"{message}")

    await ctx.message.delete()



@client.command()

async def play(ctx, url):

    if ctx.voice_client is None:

        await ctx.author.voice.channel.connect()

    else:

        ctx.voice_client.stop()

    FFMPEG_OPTIONS = {

      'before_options':

      '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',

      'options': '-vn'

    }

    YDL_OPTIONS = {'format': "bestaudio"}

    vc = ctx.voice_client



    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:

      info = ydl.extract_info(url, download=False)

      url2 = info['formats'][0]['url']

      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

      vc.play(source)

@client.command()

async def pause(ctx):

    await ctx.voice_client.pause()

    await ctx.send("Paused")

@client.command()

async def resume(ctx):

    await ctx.voice_client.resume()

    await ctx.send("Resumed")

@client.command()
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    await ctx.send(f"my ping is {ping}ms")

with open("config.json") as f:
    data = json.load(f)

token = data["bot-token"]

client.run(token)