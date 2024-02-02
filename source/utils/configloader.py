import json
import sys
from discord.ext import commands

with open("config.json", "r") as file:
    configData = json.load(file)

# main
mainConfig = configData["Config"]
selfbotToken = mainConfig["selfbotToken"]
selfbotPrefix = mainConfig["selfbotPrefix"]
webhookURL = mainConfig["webhookURL"]
authedUserIDs = mainConfig["authedUsers"]


# autoclaimer
autoclaimConfig = configData["Autoclaimer"]
addedDelay = autoclaimConfig["addedDelay"]
isRetry = autoclaimConfig["enableRetry"]
isAutoLeave = autoclaimConfig["enableAutoLeave"]
isDetections = autoclaimConfig["detections"]
claimLogging = autoclaimConfig["claimLogging"]
autoGetChannels = autoclaimConfig["autoGetAllConfigChannels"]
isAutoShout = autoclaimConfig["autoShout"]["isEnabled"]
shoutMessage = autoclaimConfig["autoShout"]["shoutMessage"]
SFinderChannels = autoclaimConfig["finderChannelsIDs"]

# autoswitch
autoswitchConfig = configData["AutoSwitch"]
isSwitchEnabled = autoswitchConfig["isEnabled"]
switchAfter = autoswitchConfig["switchAfter"]
isSwitchLogging = autoswitchConfig["switchLogging"]
accountConfig = autoswitchConfig["accountConfig"]

# initial
browserCookie = 213178712389
sys.path.insert(0, 'discord.py-self')
lastGroups = [0, 0, 0]
isClaiming = False
claimedGroups = 0
joinAttempts = 0
visionaryXVersion = "4.5.0"
selectedChannels = []
finderChannels = []
initialSwitchAfter = switchAfter
combos = list(accountConfig.keys())
currentCookieIndex = 1
visionaryBot = commands.Bot(command_prefix=selfbotPrefix, help_command=None, self_bot=True)
startURLs = {
    1: "https://www.roblox.com/groups/",
    2: "https://roblox.com/groups/",
    3: "roblox.com/groups/",
    4: "www.roblox.com/groups/",
    5: "https://roproxy.com/groups/",
    6: "https://www.roproxy.com/groups/"
}
