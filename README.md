
# VisionaryX AC

Most user-friendly & fastest roblox autoclaimer - for autoclaiming unclaimed roblox groups. It utilizes discord.py-self, to receive groups from feeds.

# Configuration
First, you want to configure config.json, which you will be able to set the following-
- discord user token (for selfbot)
- selfbot prefix (for running commands)
- webhook url (where all logs will be sent)
- authed users (all users that can run commands)
- autoclaimer delay (adds a delay between the join & claim)
- detections (sends group information after claim)
- retry (will retry if a unknown error occurs)
- claim logs (enables logs for autoclaimer)
- autoshout (will change group wall automatically after claim - can set custom message)
- auto get all config channels (automatically connects to all channels on startup)
- finder channel ids (put all channel ids that you want to claim from)
- autoswitch (autoswitches accounts)
- switch after (recommended to keep at 11, since thats the rate limit)
- switch logging (account switch logs)
- account config (more on that below)


Now to setup the account config, you want to put your cookies into cookies.txt, each one on a new line, and then run setupCookies.py (python setupCookies.py)

# Start up
To start the autoclaimer, run start.py (python start.py) - it will then load and attempt to connect to the discord token. You will then be prompted with a screen to choose what channel you want to connect to, there will be a option to pick all channels. This prompt will not show up if you have autoGetAllConfigChannels enabled, as it will just connect to all of the channels on startup. 
Once running, you can use >>help (or whatever prefix you set) to see the avaliable commands, you can basically control everything via commands - this is meant to be ran 24/7, so it is very user friendly. 

# Heads-up
Use cookies that are created on the same IP address that you are running this tool from, this is to prevent captchas. - If you ever start randomly getting captchas (never happened to me), then simply change the browser cookie to an updated one, in 

# Support
My discord server is https://discord.gg/c9xyX3H93F - this tool will probably never be updated, as I am no longer continuing roblox group stuff. Feel free to join the server just incase there is updates, but please do not DM me for support on this tool. source/utils/configloader.py

