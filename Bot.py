import discord
from discord.ext import commands
import json
import aioschedule as schedule
import time
from datetime import datetime
import requests
import asyncio

#Setup
#
#Get your api keys from these links
#----------------------------------
#
#https://discord.com/developers/applications
#https://api.nasa.gov/
#
#Get your space channel id
#-------------------------
#
#Enable developer mode in discord through your settings in advanced
#Copy the id of the channel you want to the space pictures to go to everyday, by right clicking on the channel and clicking copy id.
#
#Setting up the file
#---------------
#
#Change the save location var to the location of the text file in the folder this bot is in, example(C:/Users/Username/Desktop/Bot/data.txt)
#Put your discord bot key in example(DISCORDKEY- aweu8237jewiuef8s)
#Put your nasa api key in example(NASASPIKEY- aweu8237jewiuef8s)
#Put your discord channel id in example(SPACECHANNEL- aweu8237jewiuef8s)
#

nasaKey = ""
apodUrl = 'https://api.nasa.gov/planetary/apod'

spaceChannel = ""

discordKey = " "
discordKeySet = 0

client = commands.Bot('.')
debug_mode = 1

saveLocation = 'C:/Users/Username/Desktop/Bot/data.txt' #In case your wondering this is the variable to change

def load():
    with open(saveLocation) as file:
        lines = []
        for line in file:
            if(line.find('DISCORDKEY- ' ) != -1):
                lineUpdated = line.replace('DISCORDKEY- ', '')
                global discordKey
                global discordKeySet
                discordKey = lineUpdated
                discordKeySet = 1
                print("Discord Key Has Been Set")
            if(line.find('NASASPIKEY- ' ) != -1):
                lineUpdated = line.replace('NASASPIKEY- ', '')
                global nasaKey
                nasaKey = lineUpdated
                print("Nasa Api Key Has Been Set")
            elif(line.find('SPACECHANNEL- ' ) != -1):
                lineUpdated = line.replace('SPACECHANNEL- ', '')
                global spaceChannel
                spaceChannel = lineUpdated
                print("Space channel found!")

load()

async def Apod():
    print("Getting Apod")

    global nasaKey
    global spaceChannel

    response = requests.get(apodUrl,params={
        'api_key':nasaKey
    })

    json_data = json.loads(response.text)
    image_url = json_data['url']
    image_name = json_data['title']
    image_desc = json_data['explanation']
    image_creator = json_data['copyright']
    
    channel = client.get_channel(int(nasaKey))

    embeded = discord.Embed(title=image_name + "  |  " + datetime.today().strftime('%Y-%m-%d') + "  |  " + image_creator, description=image_desc, color=0xEE8700)
    embeded.set_thumbnail(url=image_url)

    await channel.send(embed=embeded)

schedule.every().day.at("12:00").do(Apod)

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    while True:
        await schedule.run_pending()
        time.sleep(1)

def setupDiscordBot():
    print("Starting up discord bot")
    discordKeySet = 0
    client.run(discordKey)

while True:
    if(discordKeySet == 1):
        setupDiscordBot()
