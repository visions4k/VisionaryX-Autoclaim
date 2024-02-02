import json

def loadCookies(file_path):
    with open(file_path, 'r') as file:
        cookies = file.read().splitlines()
    return cookies

def updateConfig(config, account_id, new_cookies):
    account_id_str = str(account_id)
    if account_id_str in config['AutoSwitch']['accountConfig']:
        existing_cookies = config['AutoSwitch']['accountConfig'][account_id_str].get('robloxCookie', [])
        if isinstance(existing_cookies, str):
            existing_cookies = [existing_cookies]
        updated_cookies = existing_cookies + [new_cookies]
        config['AutoSwitch']['accountConfig'][account_id_str]['robloxCookie'] = updated_cookies
        print(f"added cookie for {account_id_str}")
    else:
        config['AutoSwitch']['accountConfig'][account_id_str] = {"robloxCookie": new_cookies}
        print(f"added entry for {account_id_str}")

def saveConfig(config, file_path):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

def main():
    configFile = 'config.json' 
    cookiesFile = 'cookies.txt'  
    with open(configFile, 'r') as file:
        config = json.load(file)

    cookies = loadCookies(cookiesFile)

    existing_accounts = len(config['AutoSwitch']['accountConfig'])

    for account_id, new_cookies in enumerate(cookies, start=1):
        updateConfig(config, existing_accounts + account_id, new_cookies)

    saveConfig(config, configFile)
    print("successfully loaded cookies")

if __name__ == "__main__":
    main()