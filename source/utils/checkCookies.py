import aiohttp
import asyncio
import json

async def getUserInfo(cookie):
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': cookie}) as session:
        async with session.get("https://users.roblox.com/v1/users/authenticated") as response:
            data = await response.json()
            username = data["name"]
            userID = data["id"]
    return username, userID

async def checkCookie(cookie_number, roblox_cookie):
    try:
        username, userID = await getUserInfo(roblox_cookie)
        print(f"COOKIE #{cookie_number} | VALID | USER: {username} | ID: {userID}")
    except Exception as e:
        print(f"COOKIE #{cookie_number} | INVALID")

async def runProcess(config):
    tasks = []
    for cookie_number, account_config in config['AutoSwitch']['accountConfig'].items():
        roblox_cookie = account_config.get('robloxCookie')
        if roblox_cookie:
            task = await checkCookie(cookie_number, roblox_cookie)
            tasks.append(task)  
            await asyncio.sleep(2)
    await asyncio.gather(*tasks)

def main():
    config_file_path = 'config.json' 
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    asyncio.run(runProcess(config))

if __name__ == "__main__":
    main()
