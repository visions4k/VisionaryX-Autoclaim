import requests
import asyncio
from source.utils.configloader import *
from source.utils.console import *

def getChannels():
    if autoGetChannels:
        important("Automatically getting channels")
        return [finder for finder in SFinderChannels.values() if finder]
    important("Select channel/s to claim from")
    option("0. Autoscrape Finders")
    for i in range(len(SFinderChannels)):
        option(f"{i+1}. Config Finder {i+1}")
    option(f"{len(SFinderChannels)+1}. All Config Finders")
    selectedChannels = inputt("")
    channelNumbers = [int(num.strip()) for num in selectedChannels.split(",")]  
    if '0' in selectedChannels:
        allChannels = [channel.id for channel in visionaryBot.get_all_channels() if "finder" in channel.name]
        ok(f"Scraped: {allChannels}")
        return allChannels  
    if len(SFinderChannels)+1 in channelNumbers:
        return [finder for finder in SFinderChannels.values() if finder]
    
    return [SFinderChannels.get(str(num)) for num in channelNumbers if str(num) in SFinderChannels]

def checkID(userID):
    try:
        r = requests.get("https://groups.roblox.com/v1/users/{user_id}/groups/roles".format(user_id=userID))
        r.raise_for_status()
        d = r.json()

        if "data" not in d or not isinstance(d["data"], list):
            return None, None, None
        gidData = d["data"]
        ownedG = [group for group in gidData if group["group"]["owner"]["userId"] == int(userID)]
        ownedGC = len(ownedG)
        totalGC = len(gidData)
        return ownedGC, totalGC, totalGC - ownedGC
    except requests.exceptions.RequestException as e:
        return None, None, None

def sendWebhook(message):
    global webhookURL
    embedData = {
        "author": {
            "name": "VisionaryX | v4.5",
            "icon_url": "https://media.discordapp.net/attachments/1170886490407047178/1172273007813734442/ezgif.com-crop_5.gif" 
        },
        "description": message,
        "color": 0x2b2d31,
        "footer": {"text": f"VisionaryX | {selfbotPrefix}help"},
    }
    embedData["footer"]["icon_url"] = "https://media.discordapp.net/attachments/1170886490407047178/1172273007813734442/ezgif.com-crop_5.gif"
    d = {
        "embeds": [embedData]
    }
    h = {
        "Content-Type": "application/json"
    }

    r = requests.post(webhookURL, json=d, headers=h)
    r.raise_for_status()

def extractID(link):
    return digits if (digits := ''.join(filter(str.isdigit, link))) else None

async def countingProcess():
    global claimedGroups, switchAfter
    while True:
        counter(f" {claimedGroups}")
        await asyncio.sleep(0.5)
        
def addCounter():
    global claimedGroups
    claimedGroups += 1