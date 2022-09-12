from __main__ import *
import httpx
import dateutil.parser as dp

def to_readable(string):
    global dp

    stamp = dp.parse(string)
    return stamp

try:
    response = httpx.get(f"https://api.ivr.fi/twitch/resolve/{margs[0]}").json()
    if response["banned"]:
        results.append(f"\033[0mBanned — \033[32m{response['banned']}")
    if response["displayName"]:
        results.append(f"\033[0mDisplay Name — \033[32m{response['displayName']}")
    if response["id"]:
        results.append(f"\033[0mID — \033[32m{response['id']}")
    if response["bio"]:
        results.append(f"\033[0mBio — \033[32m{response['bio']}")
    if response["partner"]:
        results.append(f"\033[0mPartner — \033[32m{response['partner']}")
    if response["affiliate"]:
        results.append(f"\033[0mAffiliate — \033[32m{response['affiliate']}")
    if response["bot"]:
        results.append(f"\033[0mBot — \033[32m{response['bot']}")
    if response["chatColor"]:
        results.append(f"\033[0mChat Color — \033[32m{response['chatColor']}")
    if response["createdAt"]:
        results.append(f"\033[0mCreated — \033[32m{to_readable(response['createdAt'])}")
    if response["updatedAt"]:
        results.append(f"\033[0mLast Updated — \033[32m{to_readable(response['updatedAt'])}")
    if response["settings"]["preferredLanguageTag"]:
        results.append(f"\033[0mLanguage — \033[32m{response['settings']['preferredLanguageTag']}")
    response = httpx.get(f"https://api.twitchdatabase.com/following/{margs[0]}").json()
    results.append(f"\033[0mFollowing — \033[32m{response['total']}")
    for follow in response["followingList"]:
        results.append(f"   ↳ {follow['login']}\033[0m since \033[32m{to_readable(follow['followed_at'])}")
except Exception as e:
    results.append(f"\033[31m{e}")
