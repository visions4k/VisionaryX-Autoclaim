import time
import aiohttp
from source.utils.configloader import *
from source.utils.extras import *
from source.utils.console import *
from source.process.processes import *

@visionaryBot.event
async def on_message(message):
    global selectedChannels, finderChannels, isClaiming, authedUserIDs
    if message.channel in finderChannels and isClaiming:
        groupLink = None
        if message.embeds:
            embed = message.embeds[0]
            if embed.url and embed.url.startswith(tuple(startURLs.values())):
                groupLink = embed.url
            elif embed.fields:
                for field in embed.fields:
                    if any(field.value.startswith(url) for url in startURLs.values()):
                        groupLink = field.value
                        break
            elif embed.title and embed.title.startswith(tuple(startURLs.values())):
                groupLink = embed.title
        else:
            urls = re.findall(r'(https?://\S+)', message.content)
            for url in urls:
                if url.startswith(tuple(startURLs.values())):
                    groupLink = url
                    break
        if groupLink:
            channelName = message.channel.name
            messageLink = message.jump_url
            groupID = extractID(groupLink)
            found(f'GID: {groupID} | From: {channelName}')
            await automateProcess(groupID, groupLink, channelName, messageLink, retries=0)
    authedUsers = authedUserIDs.values()
    if str(message.author.id) in authedUsers and message.content.startswith(selfbotPrefix):
        await visionaryBot.process_commands(message)

            
@visionaryBot.event
async def on_ready():
    global selectedChannels, finderChannels, isClaiming
    isClaiming = False
    clear()
    log(f'Bot/s Connected: {visionaryBot.user}')
    print("")
    selectedChannels = getChannels() 
    clear()
    selectedChannels = [int(id) for id in selectedChannels]  
    finderChannels = [channel for channel in visionaryBot.get_all_channels() if channel.id in selectedChannels]
    failedChannels = [id for id in selectedChannels if not any(channel.id == id for channel in finderChannels)]
    for finder in finderChannels:
        if finder:
            ok(f"Successful connection on: {finder}")
    for failed in failedChannels:
        fatal(f"Failed connection on: {failed}")
    time.sleep(3)
    await setCookie()
    clear()
    logo()
    ok("Successfully loaded")
    findersScanning = ", ".join(str(channel) for channel in finderChannels)
    log(f"Claiming from: {findersScanning}")
    print("")
    visionaryBot.loop.create_task(countingProcess())
    isClaiming = True

@visionaryBot.event
async def on_disconnect():
    fatal("Discord Connection Failed | Retrying..")
    time.sleep(1)
    while not visionaryBot.is_closed():
        try:
            await visionaryBot.run(selfbotToken)
        except Exception:
            fatal("Discord Reconnection Failed")
            return
        else:
            ok("Discord Reconnection Successful")
            break
    
@visionaryBot.command()
async def check(ctx, userID):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    ownedGs, totalGs, nonOwnedGs = checkID(userID)
    message = f"**Account Check**\n> User ID: `{userID}`\n> Owned groups: `{ownedGs}`\n> Total groups: `{totalGs}`\n> Non owned groups: `{nonOwnedGs}`"
    sendWebhook(message)
    
@visionaryBot.command()
async def toggleclaimer(ctx):
    global isClaiming, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    if isClaiming:
        isClaiming = False
        message = f"**Claimer Toggled**\n> Status: `Disabled`"
    else:
        isClaiming = True
        message = f"**Claimer Toggled**\n> Status: `Enabled`"
    sendWebhook(message)

@visionaryBot.command()
async def addcookie(ctx, cookie):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    await cookieProcess(cookie)
    username, userID = await getUserInfo(cookie)
    message = f"**Cookie Added**\n> Username: `{username}`\n> UserID: `{userID}`"
    sendWebhook(message)
    
@visionaryBot.command()
async def currentcookie(ctx):
    global currentCookieIndex, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    robloxCookie, csrfToken = await accountProcess()
    username, userID = await getUserInfo(robloxCookie)
    message = f"**Current Cookie**\n> Username: `{username}`\n> UserID: `{userID}`\n> Current Index: `{currentCookieIndex}`"
    sendWebhook(message)
    
@visionaryBot.command()
async def addfinder(ctx, channelID: int):
    global finderChannels, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    finder = visionaryBot.get_channel(channelID)
    if finder is None:
        message = f"Finder `{channelID}` does **not exist**"
    else:
        finderChannels.append(finder)
        message = f"Finder `{channelID}` **successfully** added"
    sendWebhook(message)

@visionaryBot.command()
async def removefinder(ctx, channelID: int):
    global finderChannels, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    finder = visionaryBot.get_channel(channelID)
    if finder not in finderChannels:
        message = f"Finder `{channelID}` is **not in list**"
    else:
        finderChannels.remove(finder)
        message = f"Finder `{channelID}` **successfully** removed"
    sendWebhook(message)

@visionaryBot.command()
async def changewebhook(ctx, webhook):
    global webhookURL, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    webhookURL = webhook
    sendWebhook("**Webhook successfully changed**")

@visionaryBot.command()
async def changedelay(ctx, delay):
    global addedDelay, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    await changeDelay(delay) 
    addedDelay = delay
    message = f"**Delay successfully changed**\n> Delay: `{delay}`"
    sendWebhook(message)
    
@visionaryBot.command()
async def addauthuser(ctx, userID: int):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    nextKey = str(max(int(k) for k in authedUserIDs.keys()) + 1)
    authedUserIDs[nextKey] = str(userID)
    message = f"<@{userID}> has been successfully **authorized**"
    sendWebhook(message)

@visionaryBot.command()
async def removeauthuser(ctx, userID: int):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    userID = str(userID)
    if keyToRemove := [
        key for key, value in authedUserIDs.items() if value == userID
    ]:
        authedUserIDs.pop(keyToRemove[0])
        message = f"<@{userID}> has been successfully **deauthorized**"
    else:
        message = f"<@{userID}> is not an authorized user"
    sendWebhook(message)
    
@visionaryBot.command()
async def autoleave(ctx):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    robloxCookie, csrfToken = await accountProcess()
    username, userID = await getUserInfo(robloxCookie)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://groups.roblox.com/v2/users/{userID}/groups/roles') as resp:
            d = await resp.json()
    groupListRaw = [str(group['group']['id']) for group in d['data'] if group['role']['rank'] != 255]
    groupListCount = len(groupListRaw)
    if groupListCount == 0:
        log(f'User {username} has no groups to leave')
        return
    warn(f'You are about to leaving {len(groupListRaw)} groups')
    warn('You have 10 seconds to go to press ctrl+c to cancel')
    time.sleep(10)
    userCookie = f".ROBLOSECURITY={robloxCookie}; RBXEventTrackerV2=browserid={browserCookie}"
    async with aiosonic.HTTPClient() as client:
        headers = {'Cookie': userCookie, 'X-Csrf-Token': csrfToken, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Accept': "application/json", 'Content-Type': "application/json", 'Accept-Language': "en-US,en;q=0.9", 'Accept-Encoding': "gzip, deflate, br", 'Origin': 'https://groups.roblox.com', 'Referer': 'https://groups.roblox.com/docs/index.html?urls.primaryName=Groups%20Api%20v1'}
        await autoLeave(client, userID, username, groupListRaw, headers)

    
@visionaryBot.command()
async def info(ctx):
    global claimedGroups, addedDelay, finderChannels, authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    finderNames = [channel.name for channel in finderChannels]
    finderNamesC = ', '.join(finderNames)
    userIDS = [f"<@{id}>" for id in authedUserIDs.values()]
    userIDSC = ', '.join(userIDS)
    message = f"**VisionaryX Info**\n> Version: `{visionaryXVersion}`\n> Ping: `{round(visionaryBot.latency * 1000)}ms`\n> Total Claimed: `{claimedGroups}`\n> Connected Finders: `{finderNamesC}`\n> Added Delay: `{addedDelay}`\n> Auto-Switch: `{isSwitchEnabled}`\n> Prefix: `{selfbotPrefix}`\n> Authed Users: {userIDSC}\n> Claim-Logging: `{claimLogging}`"
    sendWebhook(message)

    
@visionaryBot.command()
async def help(ctx):
    global authedUserIDs
    if str(ctx.author.id) not in authedUserIDs.values():
        return
    message = f"**VisionaryX Help**\n> `{selfbotPrefix}check <userID>` - Check a user's group stats\n> `{selfbotPrefix}switch` - Switch accounts\n> `{selfbotPrefix}addfinder <channelID>` - Add another finder connection\n> `{selfbotPrefix}removefinder <channelID>` - Remove a finder connection\n> `{selfbotPrefix}changewebhook <webhook>` - Change the webhook URL\n> `{selfbotPrefix}changedelay <delay>` - Change the join to claim delay\n> `{selfbotPrefix}addcombo <cookie>` - Adds cookie to list\n> `{selfbotPrefix}addauthuser <userID>` - Adds an authed user (can run commands)\n> `{selfbotPrefix}removeauthuser <userID>` - Remove an authed user\n> `{selfbotPrefix}autoleave` - Activates autoleave (leaves all groups you dont own)\n> `{selfbotPrefix}info` - Get info and stats"
    sendWebhook(message)

