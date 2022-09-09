from __main__ import *
import httpx, trio

async def start_users(user, parent, client, out, fls):
    if not parent["valid"]: pass
    try: resp = await client.get(f"https://late-tooth-b0bf.ocemail.workers.dev/?{parent['check_uri'].replace('{account}', user)}")
    except: pass
    else:
        if resp.status_code == int(parent["account_existence_code"]) and not resp.text.find(parent["account_existence_string"]) == -1:
            out.append(parent["check_uri"].replace("{account}", user))
        else:
            fls.append(parent["check_uri"].replace("{account}", user))

async def main_users(user, out, fls):
    global httpx, start_users, trio

    websites = httpx.get("https://raw.githubusercontent.com/WebBreacher/WhatsMyName/master/web_accounts_list.json").json()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"
    }

    client = httpx.AsyncClient(headers=headers, timeout=20)
    async with trio.open_nursery() as nursery:
        for website in websites["sites"]: nursery.start_soon(start_users, user, website, client, out, fls)
    await client.aclose()

try:
    out, fls = [], []
    trio.run(main_users, margs[0], out, fls)
    for website in out: results.append(website)
    for website in fls: fails.append(website)
except Exception as e:
    results.append(f"\033[31m{e}")