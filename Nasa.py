import discord
from PIL import Image
import glob
import requests
from io import BytesIO
from datetime import datetime, timedelta
import Utils as ut
import os
from bs4 import BeautifulSoup
import discord
import pandas as pd
import lxml

APIKEY = "NASA API KEY" #Go to https://api.nasa.gov/ and generate a API key.

#https://worldview.earthdata.nasa.gov/?v=-177.5296364461404,-19.69179208641745,51.345092435088645,90.02503107102171&l=Reference_Labels_15m(hidden),Reference_Features_15m(hidden),Coastlines_15m(hidden),GMI_Brightness_Temp_Asc(hidden),VIIRS_NOAA20_CorrectedReflectance_TrueColor(hidden),VIIRS_SNPP_CorrectedReflectance_TrueColor,MODIS_Aqua_CorrectedReflectance_TrueColor(hidden),MODIS_Terra_CorrectedReflectance_TrueColor(hidden)&lg=true&tr=geostationary&t=2023-04-21-T14%3A42%3A13Z
def EOSDID():
    pass

def Eonet():
    pass

def Apod():
    res = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={APIKEY}").json()
    return res["title"], res["url"]

def Insight():
    CW = GetCWheather()
    PW = GetPWheather()
    return CW, PW

def GetCWheather():
    res = requests.get("https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json")
    js = res.json()
    return js["soles"][0]

def GetPWheather():
    res = requests.get("https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json")
    js = res.json()
    return js["sols"][len(js["sols"])-1]

def RoverImage():

    fileName = "RoverImage" + datetime.strftime(datetime.now(), "%Y-%m-%d") + ".png"
    saveLoc = os.getcwd() + "/Images/" + fileName

    if(os.path.exists(saveLoc)):
        return saveLoc, fileName

    response = GetRoverLink(0)

    imageToShow = ""

    for p in response["photos"]:
        if(ut.isgray(p["img_src"]) == False):
            imageToShow = p["img_src"]
            print(p["camera"]["full_name"])
            break

    if(imageToShow == ""):
        imageToShow = response["photos"][0]["img_src"]

    print(imageToShow)

    imgRes = requests.get(imageToShow)

    img = Image.open(BytesIO(imgRes.content))

    img.save(saveLoc)

    return saveLoc, fileName

def GetRoverLink(Offset):
    d = datetime.strftime(datetime.now() - timedelta(Offset), "%Y-%m-%d")

    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?earth_date={d}&api_key={APIKEY}"

    response = requests.get(url).json()
    if(len(response["photos"]) == 0):
        return GetRoverLink(Offset + 1)
    else:
        return response

#https://api.nasa.gov/EPIC/archive/natural/2023/04/21/png/epic_1b_20230421021515.png?api_key=DEMO_KEY
#https://api.nasa.gov/EPIC/api/natural/date/2023-04-21?api_key=DEMO_KEY
def Epic():

    fileName = "Earth" + datetime.strftime(datetime.now(), "%Y-%m-%d") + ".gif"
    saveLoc = os.getcwd() + "/Gifs/" + fileName

    if(os.path.exists(saveLoc)):
        return saveLoc, fileName

    yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
    yesterdayformatted = datetime.strftime(datetime.now() - timedelta(1), "%Y/%m/%d")

    url = f"https://api.nasa.gov/EPIC/api/natural/date/{yesterday}?api_key={APIKEY}"
    res = requests.get(url)
    js = res.json()

    photos = []

    for r in js:
        imgRes = requests.get(f"https://api.nasa.gov/EPIC/archive/natural/{yesterdayformatted}/png/{r['image']}.png?api_key={APIKEY}")
        photos.append(Image.open(BytesIO(imgRes.content)).resize((248, 248)))

    if(len(photos) == 0):
        return "na", "na"

    photos[0].save(saveLoc, format='GIF', append_images=photos[1:], save_all=True, duration=300, loop=0)

    return saveLoc, fileName

def GenerateDailyMessage():

    CWheather, PWheather = Insight()

    PWDesc = f'''Date:      {PWheather["terrestrial_date"]}
    Sol:        {PWheather["sol"]}
    Season:     {PWheather["season"]}
    Max-Temp:   {PWheather["max_temp"]}°C
    Min-Temp:   {PWheather["min_temp"]}°C
    Pressure:   {PWheather["pressure"]}Pa
    Sunrise:    {PWheather["sunrise"]}
    Sunset:     {PWheather["sunset"]}'''

    CWDesc = f'''Date:      {CWheather["terrestrial_date"]}
    Sol:        {CWheather["sol"]}
    Max-Temp:   {CWheather["max_temp"]}°C
    Min-Temp:   {CWheather["min_temp"]}°C
    Pressure:   {CWheather["pressure_string"]}
    Sunrise:    {CWheather["sunrise"]}
    Sunset:     {CWheather["sunset"]}
    UV-Index:   {CWheather["local_uv_irradiance_index"]}'''

    MWheather = discord.Embed(title="Mars Wheather", color=0xff0008)
    MWheather.add_field(name="Latest Mars Wheather (Curiosity , Gale Crater)", value=CWDesc, inline=True)
    MWheather.add_field(name="Latest Mars Wheather (Perseverance , Jezero Crater)", value=PWDesc, inline=True)
    
    Title, AImgUrl = Apod()

    ApodEmbed = discord.Embed(title="Astronomy Picture of the Day (" + Title + ")", color=0xff0008)
    ApodEmbed.set_image(url=AImgUrl)
    
    EImgLoc, EImgName = Epic()
    if(EImgLoc != "na"):
        EImgObj = discord.File(EImgLoc, filename=EImgName)

        EarthEmbed = discord.Embed(title="Earth Yesterday", color=0xff0008)
        EarthEmbed.set_image(url="attachment://" + EImgName)
    else:
        EImgObj = "na"
        EarthEmbed = discord.Embed(title="No Earth Satellite Images Today", color=0xff0008)

    RImgDir, FNAME = RoverImage()
    RImgObj = discord.File(RImgDir, filename=FNAME)

    RoverEmbed = discord.Embed(title="Most Recent Perseverance Photo", color=0xff0008)

    RoverEmbed.set_image(url="attachment://" + FNAME)
    
    return RoverEmbed, RImgObj, EarthEmbed, EImgObj, MWheather, ApodEmbed