import aiosonic
import aiohttp
import re
import time
import math
from source.utils.configloader import *
from source.utils.console import *
from source.utils.extras import *
from source.utils.detections import Detections
    
async def changeDelay(delay):
    global addedDelay
    addedDelay = delay
    with open("config.json", "r") as file:
        config = json.load(file)
        config["Autoclaimer"]["addedDelay"] = delay
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
        
    
async def cookieProcess(cookie):
    global accountConfig
    with open("config.json", "r") as file:
        config = json.load(file)
    newAccIndex = str(len(config["AutoSwitch"]["accountConfig"]) + 1)
    config["AutoSwitch"]["accountConfig"][newAccIndex] = {
        "robloxCookie": cookie
    }
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    accountConfig = config["AutoSwitch"]["accountConfig"]

    
async def accountProcess():
    global currentCookieIndex, switchAfter, accountConfig, joinAttempts, robloxCookie
    if autoswitchConfig["isEnabled"] and joinAttempts >= switchAfter:
        currentCookieIndex += 1
        switchAfter += initialSwitchAfter
        log(f"Autoswitch Process | Cookie {currentCookieIndex}")
        sendWebhook(f"**Autoswitch Process**\n> Switched to `cookie {currentCookieIndex}`")
    if str(currentCookieIndex) not in accountConfig:
        currentCookieIndex = 1
    account = accountConfig[str(currentCookieIndex)]
    robloxCookie = account["robloxCookie"]
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': robloxCookie}) as session:
        async with session.post("https://groups.roblox.com") as response:
            csrfToken = response.headers['x-csrf-token']
    return robloxCookie, csrfToken

async def setCookie():
    global robloxCookie
    robloxCookie, csrfToken = await accountProcess()
    
async def getUserInfo(cookie=None):
    global robloxCookie
    if cookie is None:
        cookie = robloxCookie
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': cookie}) as session:
        async with session.get("https://users.roblox.com/v1/users/authenticated") as response:
            d = await response.json()
            username = d["name"]
            userID = d["id"]
    
    return username, userID
        
async def autoLeave(client, userID, username, groupListRaw, headers):
    groupListCount = len(groupListRaw)
    groupList = ','.join(groupListRaw)
    groupIDs = groupList.split(',')
    successful = await leaveProcess(client, userID, headers, groupIDs)
    message = f"**Leave Process**\n> Left `{successful}/{groupListCount}`\n> Username: `{username}`\n> User ID: `{userID}`"
    ok(f"{successful}/{groupListCount} | Autoleave Process | UserID: {userID}")
    sendWebhook(message) 
    
    
async def maxProcess(groupID, groupLink, channelName, messageLink):
    global robloxCookie, joinAttempts, currentCookieIndex
    username, userID = await getUserInfo()
    log(f"Max Group Process | Acc: {username} | Switching Cookie..")
    with open("config.json", "r") as configFile:
        configData2 = json.load(configFile)
    accountConfig2 = configData2["AutoSwitch"]["accountConfig"]
    for key in list(accountConfig2.keys()):
        if key.isdigit() and accountConfig2[key].get("robloxCookie") == robloxCookie:
            del accountConfig2[key]
    accountConfig2 = {str(i + 1): config for i, config in enumerate(val for key, val in accountConfig2.items() if key.isdigit())}
    configData2["AutoSwitch"]["accountConfig"] = accountConfig2
    with open("config.json", "w") as configFile:
        json.dump(configData2, configFile, indent=4)
    with open('outputs/maxedcookies.txt', 'a') as file:
        file.write(f"{username}:{userID} | {str(robloxCookie)}" + '\n')
    joinAttempts = math.ceil(joinAttempts / initialSwitchAfter) * initialSwitchAfter
    await automateProcess(groupID, groupLink, channelName, messageLink, retries=1)
      
async def shoutProcess(client, headers, groupID):
    r = await client.patch(f'https://groups.roblox.com/v1/groups/{groupID}/status', headers=headers, json={"message": shoutMessage})
    if r.status_code == 200:
        okreq(f"Shout Process | GID: {groupID}")
    else:
        fatalreq(f"Shout Process | GID: {groupID}", r.status_code)
    
async def leaveProcess(client, userID, headers, groupIDs):
    global robloxCookie
    if not isinstance(groupIDs, list):
        groupIDs = [groupIDs]
    successful = 0
    if userID == 0:
        username, userID = await getUserInfo()
    for groupID in groupIDs: 
        r = await client.delete(f'https://groups.roblox.com/v1/groups/{groupID}/users/{userID}' , headers=headers)
        if r.status_code == 200:
            okreq(f"Leave Process | GID: {groupID}")
            successful += 1
        else:
            fatalreq(f"Leave Process | GID: {groupID}", r.status_code)
        with open('outputs/left.txt', 'a') as file:
            file.write(str(groupID) + '\n')
    return successful
    
                    
async def joinProcess(client, groupID, headers, groupLink, channelName, messageLink, retries=0):
    global joinAttempts
    r = await client.post(f'https://groups.roblox.com/v1/groups/{groupID}/users', headers=headers)
    joinAttempts += 1
    if r.status_code == 200:
        okreq(f"Join Process | GID: {groupID}")
        return True
    elif r.status_code == 401:
        joinAttempts = math.ceil(joinAttempts / initialSwitchAfter) * initialSwitchAfter
    else:
        rMsg = json.loads(await r.content()).get('errors')[0].get('message')
        if rMsg.startswith("Too many"):
            joinAttempts = math.ceil(joinAttempts / initialSwitchAfter) * initialSwitchAfter
            if retries > 1:
                return False
            if isRetry:
                await automateProcess(groupID, groupLink, channelName, messageLink, retries=retries+1)
        if rMsg.startswith("You are already in the maximum number"):
            await maxProcess(groupID, groupLink, channelName, messageLink)
        elif claimLogging:
            message = f"**Failed joining**\n> Group ID: `{groupID}`\n> Status: `{r.status_code}`\n> Response: `{rMsg}`"
            sendWebhook(message)
        return False
        
    
async def claimProcess(client, groupID, headers):
    r = await client.post(f'https://groups.roblox.com/v1/groups/{groupID}/claim-ownership', headers=headers)
    if r.status_code == 200:
        okreq(f"Claim Process | GID: {groupID}")
        return True
    else:
        fatalreq(f"Claim Process | GID: {groupID}", r.status_code)
        if isAutoLeave:
            userID = 0
            await leaveProcess(client, userID, headers, groupID)
        rMsg = json.loads(await r.content()).get('errors')[0].get('message')
        if claimLogging:
            message = f"**Failed claiming**\n> Group ID: `{groupID}`\n> Status: `{r.status_code}`\n> Response: `{rMsg}`"
            sendWebhook(message)
            return False
        return False
    
async def automateProcess(groupID, groupLink, channelName, messageLink, retries=0):
    global lastGroups, addedDelay, robloxCookie
    if groupID in lastGroups and retries == 0:
        warn(f"Duplicated GID: {groupID}")
        return
    timerStart = time.perf_counter()
    lastGroups = [groupID] + lastGroups[:2]
    robloxCookie, csrfToken = await accountProcess()
    userCookie = f".ROBLOSECURITY={robloxCookie}; RBXEventTrackerV2=browserid={browserCookie}"
    async with aiosonic.HTTPClient() as client:
        headers = {'Cookie': userCookie, 'X-Csrf-Token': csrfToken, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Accept': "application/json", 'Content-Type': "application/json", 'Accept-Language': "en-US,en;q=0.9", 'Accept-Encoding': "gzip, deflate, br", 'Origin': 'https://groups.roblox.com', 'Referer': 'https://groups.roblox.com/docs/index.html?urls.primaryName=Groups%20Api%20v1'}
        if await joinProcess(client, groupID, headers, groupLink, channelName, messageLink):
            time.sleep(int(addedDelay))
            if await claimProcess(client, groupID, headers):
                timerEnd = time.perf_counter()
                if isAutoShout:
                    await shoutProcess(client, headers, groupID)
                claimTime = (timerEnd - timerStart) * 1000
                addCounter()
                with open('outputs/claimed.txt', 'a') as file:
                    file.write(groupID + '\n') 
                if claimLogging:
                    message = f"**Successful Autoclaim**\n> [**Group Redirect**]({groupLink})\n> Group ID: `{groupID}`\n> Claim Speed: `{claimTime:.2f}ms`"
                    sendWebhook(message) 
                if isDetections:
                    await Detections(robloxCookie).sendDetections(groupID)