import os, sys, json, time, random, string, ctypes, logging
import threading
import concurrent.futures

try:
    import requests
    import colorama
    import pystyle
    import datetime
    import capmonster_python
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install capmonster_python")

from colorama import Fore, Style
from tls_client import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from capmonster_python import HCaptchaTask
from concurrent import futures
from threading import Lock

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

joined = 0
solved = 0
errors = 0
rules = 0

tokens = len(open('tokens.txt').readlines())

ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Token Joiner | Joined : {joined} | Solved : {solved} | Errors : {errors} | Accepted Rules : {rules} | Total Tokens : {tokens} | .gg/hcuxjpSfkU')

def update_console_title():
    ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Token Joiner | Joined : {joined} | Solved : {solved} | Errors : {errors} | Accepted Rules : {rules} | Total Tokens : {tokens} | .gg/hcuxjpSfkU')

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def ui():
    Write.Print("""
\t ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▄            ▄█  ▄▀▀▀▀▄   ▄▀▀█▀▄    ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
\t█    █  ▐ █      █ █  █ ▄▀ ▐  ▄▀   ▐ █  █ █ █      ▄▀▀▀█▀ ▐ █      █ █   █  █  █  █ █ █ ▐  ▄▀   ▐ █   █   █ 
\t▐   █     █      █ ▐  █▀▄    █▄▄▄▄▄  ▐  █  ▀█     █    █    █      █ ▐   █  ▐  ▐  █  ▀█   █▄▄▄▄▄  ▐  █▀▀█▀  
\t   █      ▀▄    ▄▀   █   █   █    ▌    █   █      ▐    █    ▀▄    ▄▀     █       █   █    █    ▌   ▄▀    █  
\t ▄▀         ▀▀▀▀   ▄▀   █   ▄▀▄▄▄▄   ▄▀   █         ▄   ▀▄    ▀▀▀▀    ▄▀▀▀▀▀▄  ▄▀   █    ▄▀▄▄▄▄   █     █   
\t█                  █    ▐   █    ▐   █    ▐          ▀▀▀▀            █       █ █    ▐    █    ▐   ▐     ▐   
\t▐                  ▐        ▐        ▐                               ▐       ▐ ▐         ▐                  
""", Colors.green_to_white, interval=0.0000)
ui()
print(f"\n")
time.sleep(3)

def captcha_bypass(token, url, key, captcha_rqdata):
    global solved
    with open("config.json") as dsc_ez:
        config = json.load(dsc_ez)
        startedSolving = time.time()
        capmonster = HCaptchaTask(config['capmonster_key'])
        task_id = capmonster.create_task(url, key, is_invisible=True, custom_data=captcha_rqdata)
        result = capmonster.join_task_result(task_id)
        response = result.get("gRecaptchaResponse")
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pretty}Solved {gray}|{pink} {yellow}{response[-32:]} {gray}In {yellow}{round(time.time()-startedSolving)}s")
        solved += 1
        update_console_title()
        return response

def nonce():
    date = datetime.datetime.now()
    unixts = time.mktime(date.timetuple())
    return str((int(unixts)*1000-1420070400000)*4194304)

def join(token):
    global joined, solved, errors, rules
    with open("config.json") as jn:
        check = json.load(jn)
        invite_code = check.get('invite')
    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    session = Session(client_identifier="chrome_114", random_tls_extension_order=True)

    if proxy.count(":") == 1:
        session.proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }
    elif proxy.count(":") == 3:
        username, password, ip, port = proxy.split(":")
        session.proxies = {
            "http": f"http://{username}:{password}@{ip}:{port}",
            "https": f"http://{username}:{password}@{ip}:{port}"
        }

    headers_finger = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
            'X-Track': 'eyJvcyI6IklPUyIsImJyb3dzZXIiOiJTYWZlIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKElQaG9uZTsgQ1BVIEludGVybmFsIFByb2R1Y3RzIFN0b3JlLCBhcHBsaWNhdGlvbi8yMDUuMS4xNSAoS0hUTUwpIFZlcnNpb24vMTUuMCBNb2JpbGUvMTVFMjQ4IFNhZmFyaS82MDQuMSIsImJyb3dzZXJfdmVyc2lvbiI6IjE1LjAiLCJvc192IjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfZG9tYWluX2Nvb2tpZSI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOiJzdGFibGUiLCJjbGllbnRfZXZlbnRfc291cmNlIjoic3RhYmxlIn0',
        }

    response = session.get('https://discord.com/api/v9/experiments', headers=headers_finger)
    if response.status_code == 200:
        data = response.json()
        fingerprint = data["fingerprint"]
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pink}Got Fingerprint {gray}| {green}{fingerprint}")
    else:
        errors += 1

    headers = {
        "authorization": token,
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkzLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTMuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTAwODA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        "sec-fetch-dest": "empty",
        "x-debug-options": "bugReporterEnabled",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "accept": "*/*",
        "accept-language": "en-GB",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
        "TE": "trailers",
        "x-fingerprint": fingerprint
    }

    response = session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers)
    if response.status_code == 400:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({magenta}${gray}) {pretty}Solving Captcha {gray}| {green}{token[:50]}******")
        payload = {
            "captcha_key": captcha_bypass(token, "https://discord.com", f"{response.json()['captcha_sitekey']}", response.json()['captcha_rqdata']), 'captcha_rqtoken': response.json()['captcha_rqtoken']
        }
        newresponse = session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers, json=payload)
        if newresponse.status_code == 200:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Token Joined Successfully {gray}|{cyan} {token[:50]}*****")
            joined += 1
            b = newresponse.json()
            server_id = b["guild"]["id"]
            if 'show_verification_form' in b:
                bypass_rules = session.get(f"https://discord.com/api/v9/guilds/{server_id}/member-verification?with_guild=false", headers=headers).json()
                accept_rules = session.get(f"https://discord.com/api/v9/guilds/{server_id}/requests/@me", headers=headers, json=bypass_rules)
                if accept_rules.status_code == 201 or accept_rules.status_code == 204:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Token Accepted Rules {gray}|{cyan} {token[:50]}*****")
                    rules += 1
                else:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Token Failed Accepting Rules {gray}| {cyan}{token[:50]}*****")
                    errors += 1
    elif response.status_code == 200:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Token Joined Successfully {gray}|{cyan} {token[:50]}*****")
        joined += 1
        b = response.json()
        server_id = b["guild"]["id"]
        if 'show_verification_form' in b:
            bypass_rules = session.get(f"https://discord.com/api/v9/guilds/{server_id}/member-verification?with_guild=false", headers=headers).json()
            accept_rules = session.get(f"https://discord.com/api/v9/guilds/{server_id}/requests/@me", headers=headers, json=bypass_rules)
            if accept_rules.status_code == 201 or accept_rules.status_code == 204:
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Token Accepted Rules {gray}|{cyan} {token[:50]}*****")
                rules += 1
            else:
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Token Failed Accepting Rules {gray}| {cyan}{token[:50]}*****")
                errors += 1
    else:
        time_rn = get_time_rn()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Token Failed To Join {gray}| {cyan}{token[:50]}*****")
        errors += 1

def main():
    with open('tokens.txt', 'r') as file:
        tokens = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(join, token) for token in tokens]
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

main()

with open("config.json") as discord_gay:
    que_onda_eres_bobo = json.load(discord_gay)
    check = que_onda_eres_bobo.get('change_nickname')
    if check == "y" or check == "yes":
        def get_guild_id_from_invite(invite_link):
            invite_key = invite_link.split('/')[-1]
            response = requests.get(f'https://discord.com/api/v9/invites/{invite_key}')
            if response.status_code == 200:
                guild_id = response.json()['guild']['id']
                return guild_id
            else:
                return None

        with open("config.json") as penis:
            data = json.load(penis)
            code = data.get('invite')
        invite_link = f'https://discord.gg/{code}'
        guild_id = get_guild_id_from_invite(invite_link)

        def nicker():
            def nicker2(server, nickname, token):
                headers = {
                    "authorization": token,
                    "accept": "*/*",
                    'accept-encoding': 'gzip, deflate, br',
                    "accept-language": "en-GB",
                    "content-length": "90",
                    "content-type": "application/json",
                    "origin": "https://discord.com",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
                    "x-debug-options": "bugReporterEnabled",
                    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI0NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InNrIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTkwMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
                }
                req = requests.patch(f"https://discord.com/api/v9/guilds/{server}/members/@me/nick", headers=headers,
                    json={
                        "nick": nickname
                    }
                )
                if req.status_code == 200:
                    time_rn = get_time_rn()
                    print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Successfully Changed Nickname {gray}|{cyan} {token[:50]}*****')
                if req.status_code != 200:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Error Changing Nickname {gray}| {cyan}{token[:50]}*****")
            tokens = open("tokens.txt", "r").read().splitlines()
            server = get_guild_id_from_invite(invite_link)
            with open("config.json") as pussy:
                omg = json.load(pussy)
                nick = omg.get('nickname')
            for token in tokens:
                threading.Thread(target=nicker2, args=(server, nick, token)).start()
                time.sleep(1)
        nicker()
        time_rn = get_time_rn()
        input(f"\n{reset}[ {cyan}{time_rn}{reset} ] {gray}({blue}#{gray}) {pretty}Press ENTER : ")
        exit()
    else:
        time_rn = get_time_rn()
        input(f"\n{reset}[ {cyan}{time_rn}{reset} ] {gray}({blue}#{gray}) {pretty}Press ENTER : ")
        time.sleep(1)
        exit()