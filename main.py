import requests
from lxml.html import fromstring
import re
import json
import math
import time
import sys
from multiprocessing.dummy import Pool as ThreadPool


def RemTrash(string):
    string = re.sub("^[\u00a0 \s]*", "", string)
    string = re.sub("[\s\u00a0 ]*$", "", string)
    return string


def GetOwnedGames(steam_api_key, steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_id}&format=json&include_appinfo=1"
    response = requests.get(url)

    try:
        games = response.json()["response"]["games"]
        return games
    except Exception as e:
        print("Error: Failed to fetch games:", str(e))
        return None


def GetGameSpace(appid):
    result = 0
    head = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "mature_content=1; birthtime=252442801; lastagecheckage=1-January-1978",
    }

    try:
        html = requests.get(f"https://store.steampowered.com/app/{appid}", headers=head).text.lower()
        page = fromstring(html)
    except Exception as e:
        print(f"Error: Failed to fetch store page for AppID {appid}: {e}")
        return {"size": 0, "appid": appid, "name": f"AppID {appid}"}

    pattern_arr = [
        "жесткий диск",
        "место на диске",
        "hard drive",
        "hard disk space",
        "место на жестком диске",
        "места на жестком диске"
    ]
    pattern_str = ' or '.join([f"contains(text(),'{p}')" for p in pattern_arr])
    space_obj = page.xpath(f".//li/strong[{pattern_str}]")

    if space_obj:
        space_obj_n = space_obj[0].getparent()
        space_obj_n = ''.join(space_obj_n.xpath(".//text()"))

        try:
            if(space_obj_n.replace(" ", "")[-2:] == ":\r" or space_obj_n.replace(" ", "")[-1:] == ':'):
                space_obj_n = ''.join(space_obj[1].getparent().xpath(".//text()"))
        except:
            space_obj_n = ''.join(space_obj[0].getparent().xpath(".//text()"))
        space_obj = space_obj_n

    else:
        match = re.search("[\\,\\;][\\s]([^,;]*?на ж[ёе]стком диске)", html)
        if not match:
            match = re.search("[\\,\\;][\\s]([^,;]*?на диске)", html)
        if match:
            space_obj = match.group(1)

    if space_obj:
        try:
            space_obj = RemTrash(space_obj.replace(",", "."))
            digits = ''.join(ele for ele in space_obj if ele.isdigit() or ele == '.')
            digits = re.sub("^[\\.]*", "", digits)
            digits = re.sub("[\\.]*$", "", digits)
            digits = float(digits)

            if any(x in space_obj for x in ["мб", "mb", "megabytes"]):
                digits = digits / 1000
            result = digits
        except:
            print(f"Error: Failed to parse space for AppID {appid}")

    return {"size": result, "appid": appid}


def GetSumSpace(games_array, thread_num=4, show_progress=False):
    summary = 0
    pool = ThreadPool(thread_num)
    seed = [(game['appid'], game['name']) for game in games_array]

    def wrapped(appid_name):
        appid, name = appid_name
        result = GetGameSpace(str(appid))
        print(f"{name}: {result['size']:.2f} GB")
        return result

    result = pool.map(wrapped, seed)

    for r in result:
        if r['size'] > 150:
            print(json.dumps({"appid": r['appid'], "size error": r['size']}, ensure_ascii=False))
        else:
            summary += r['size']

    if summary > 1000:
        summary /= 1000
        summary = round(summary, 2)
        return f"{summary} ТБ"
    return f"{round(summary, 2)} ГБ"


def main():
    steam_api_key = input("Enter your Steam Web API key: ").strip()
    steam_id = input("Enter your SteamID: ").strip()

    games = GetOwnedGames(steam_api_key, steam_id)

    if not games:
        print("Error: failed to get the list of games.")
        return

    total_space = GetSumSpace(games, thread_num=16, show_progress=False)
    print(f"\nTotal library size: {total_space}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
