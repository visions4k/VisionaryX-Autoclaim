import json
import aiosonic
from datetime import datetime
from source.utils.configloader import *


class Detections:
    def __init__(self, cookie):
        self.cookie = cookie
        self.client = aiosonic.HTTPClient()

    async def getRequest(self, url, headers=None):
        try:
            r = await self.client.get(url, headers=headers)
            return await r.json()
        except Exception as e:
            print(e)

    async def getInfo(self, gid):
        try:
            url = f"https://groups.roblox.com/v1/groups/{gid}"
            d = await self.getRequest(url)
            return d.get("name"), d.get("memberCount")
        except Exception as e:
            return "error", "error"

    async def getFunds(self, gid):
        try:
            headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
            url = f"https://economy.roblox.com/v1/groups/{gid}/currency"
            d = await self.getRequest(url, headers=headers)
            return d.get("robux")
        except Exception as e:
            return "error"

    async def getPFunds(self, gid):
        try:
            headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
            today = datetime.now().strftime("%Y-%m-%d")
            url = f"https://economy.roblox.com/v1/groups/{gid}/revenue/summary/{today}"
            d = await self.getRequest(url, headers=headers)
            return d.get("pendingRobux")
        except Exception as e:
            return "error"


    async def getGames(self, gid):
        try:
            url = f"https://games.roblox.com/v2/groups/{gid}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc"
            d = await self.getRequest(url)
            games = d.get("data", [])
            groupVisits = sum(game.get("placeVisits", 0) for game in games)
            groupGames = len(games)
            return groupGames, groupVisits
        except Exception as e:
            return "error", "error"
        
    async def shutdown(self):
        await self.client.shutdown() 

    async def processGroup(self, gid):
        groupName, groupMem = await self.getInfo(gid)
        groupFunds = await self.getFunds(gid)
        groupPFunds = await self.getPFunds(gid)
        groupGames, groupVisits = await self.getGames(gid)
        await self.shutdown()
        return gid, {
            "name": groupName,
            "members": groupMem,
            "funds": groupFunds,
            "fundsPending": groupPFunds,
            "games": groupGames,
            "visits": groupVisits
        }
    
    async def sendDetections(self, gid):
        _, data = await self.processGroup(gid)
        embedData = {
            "color": 0x2b2d31,
            "footer": {"text": f"VisionaryX | Detections"},
            "description": f"**ID:** `{gid}`",
            "fields": [
                {"name": "Name", "value": f"`{data['name']}`", "inline": True},
                {"name": "Members", "value": f"`{data['members']}`", "inline": True},
                {"name": "Funds", "value": f"`{data['funds']}`", "inline": True},
                {"name": "Pending", "value": f"`{data['fundsPending']}`", "inline": True},
                {"name": "Games", "value": f"`{data['games']}`", "inline": True},
                {"name": "Visits", "value": f"`{data['visits']}`", "inline": True}
            ]
        }
        embedData["footer"]["icon_url"] = "https://media.discordapp.net/attachments/1170886490407047178/1172273007813734442/ezgif.com-crop_5.gif"       
        await aiosonic.HTTPClient().post(webhookURL, json={"embeds": [embedData]}, headers={"Content-Type": "application/json"})
        await aiosonic.HTTPClient().shutdown()
        

        
        
