import discord
from discord.ext import commands
import Nasa as NASA

intents = discord.Intents.default()
intents.members = True

bot  = commands.Bot(command_prefix='/', intents=intents)

discordBotToken = 'BOT TOKEN' #After making a discord bot and inviting it to your server. Get its token from the developer portal.
spaceChannel = 1099480336364220446 #Put space channel id here (This can be gotten with developer mode and right clicking the channel. Then press copy id.)

@bot.event
async def on_ready():
    print(f"Bot Ready {bot .user}")
    await send()

async def send():
    channel = bot.get_channel(spaceChannel)

    RoverEmbed, RoverImage, EarthEmbed, EarthImage, MarsWheather, ApodEmbed = NASA.GenerateDailyMessage()

    await channel.send(embed=ApodEmbed)
    await channel.send(embed=MarsWheather)
    await channel.send(file=RoverImage, embed=RoverEmbed)
    if(EarthImage != "na"):
        await channel.send(file=EarthImage, embed=EarthEmbed)

    exit()
    #await ctx.send(f"Pong! {round(bot .latency * 1000)}ms.")

bot .run(discordBotToken)