from __main__ import *
import httpx
import dateutil.parser as dp

def to_readable(string):
    global dp

    stamp = dp.parse(string)
    return stamp

def to_timestamp(string):
    global dp

    stamp = dp.parse(string)
    return math.trunc(stamp.timestamp())

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

try:
    response = httpx.post("https://users.roblox.com/v1/usernames/users", data={"usernames": [" ".join(margs)]}).json()
    id = str(response["data"][0]["id"])
    response = httpx.get("https://users.roblox.com/v1/users/" + id).json()
    response2 = httpx.post("https://presence.roblox.com/v1/presence/users", data={"userIds": [int(id)]}).json()
    lastOnline = response2["userPresences"][0]["lastOnline"]
    if to_timestamp(lastOnline) == to_timestamp(response["created"]):
        try:
            response2 = httpx.get("https://api.roblox.com/users/" + id + "/onlinestatus").json()
            lastOnline = response2["LastOnline"]
        except: pass
    results.append(f"\033[0mLink — \033[32mhttps://roblox.com/users/{id}")
    if response["displayName"] != response["name"]:
        results.append(f"\033[0mDisplay Name — \033[32m{response['displayName']}")
    if response["id"]:
        results.append(f"\033[0mId — \033[32m{response['id']}")
    if response["isBanned"]:
        results.append(f"\033[0mBanned — \033[32m{response['isBanned']}")
    results.append(f"\033[0mCreated — \033[32m{to_readable(response['created'])}")
    results.append(f"\033[0mLast Updated — \033[32m{to_readable(lastOnline)}")
    description = response["description"]
    if description:
        results.append(f"\033[0mDescription — \033[32m{description}")
    response, response2, response3 = httpx.get("https://friends.roblox.com/v1/users/" + id + "/followers/count").json(), httpx.get("https://friends.roblox.com/v1/users/" + id + "/followings/count").json(), httpx.get("https://friends.roblox.com/v1/users/" + id + "/friends/count").json()
    results.append(f"\033[0mFriends — \033[32m{response3['count']}")
    results.append(f"\033[0mFollowers — \033[32m{response['count']}")
    results.append(f"\033[0mFollowings — \033[32m{response2['count']}")
    response, response2, response3 = httpx.get("https://inventory.roblox.com/v1/users/" + id +"/items/asset/18824203/is-owned").text, httpx.get("https://inventory.roblox.com/v1/users/" + id +"/items/asset/1567446/is-owned").text, httpx.get("https://inventory.roblox.com/v1/users/" + id +"/items/asset/102611803/is-owned").text
    verified = "18824203" if response == "true" else "false"
    if verified == "false": verified = "1567446" if response2 == "true" else "false"
    if verified == "false": verified = "102611803" if response3 == "true" else "false"
    if verified != "false":
        results.append(f"\033[0mVerified — \033[32mhttps://roblox.com/catalog/{verified}")
    response = httpx.get("https://accountinformation.roblox.com/v1/users/" + id + "/roblox-badges").json()
    if 1 in [badge["id"] for badge in response]:
        results.append(f"\033[0mAdmin — \033[32mTrue")
    response = httpx.get("https://groups.roblox.com/v1/users/" + id + "/groups/roles").json()
    for group in response["data"]: 
        if group["group"]["id"] == 2868472 and group["role"]["id"] == 19734284:
            results.append(f"\033[0mIntern — \033[32mTrue")
    possible = []
    for query in re.findall(DISCORD_FORMAT, description):
        query = str(query).split("(")[1].split("',")[0].split("'")[1]
        if query not in possible:
            possible.append(query)
    response = httpx.post("https://api.ropro.io/getUserInfoTest.php?userid=" + id).json()
    if response["reputation"]:
        results.append(f"\033[0mRopro Reputation — \033[32m{response['reputation']}")
    if response["tier"] != "none":
        results.append(f"\033[0mRopro Tier — \033[32m{response['tier'][:1].upper()}{response['tier'].split('_')[0][1:]}")
    if response["subscribed_for"] != "none":
        results.append(f"\033[0mRopro Subscribed For — \033[32m{response['subscribed_for']}")
    if response["user_since"] != "none":
        results.append(f"\033[0mRopro User For — \033[32m{response['user_since']}")
    if not response["discord"] in possible and not response["discord"] == "" and bool(re.fullmatch(DISCORD_FORMAT, response["discord"])): 
        possible.append(response["discord"])
    for poss in possible:
        results.append(f"\033[0mPossible Discord — \033[32m{rreplace(poss, ' ', '#', 1)}")
    names = []
    try:
        data = httpx.get("https://users.roblox.com/v1/users/" + id + "/username-history?limit=100&sortOrder=Desc").json()
        for name in data["data"]: 
            if name["name"] not in names and name != " ".join(margs):
                names.append(name["name"])
        while data["nextPageCursor"]:
            try:
                data = httpx.get("https://users.roblox.com/v1/users/" + id + "/username-history?limit=100&sortOrder=Desc&cursor=" + data["nextPageCursor"]).json()
                for name in data["data"]: 
                    if name["name"] not in names and name != " ".join(margs):
                        names.append(name["name"])
            except: pass
    except:
        try:
            data = httpx.get("https://rblx.trade/api/v1/user/profile?userId=" + id).json()
            for name in data["profileHeader"]["PreviousUserNames"].split("\r\n"): 
                if name not in names and name != " ".join(margs):
                    names.append(name)
        except: pass
    for name in names:
        results.append(f"\033[0mPast Username — \033[32m{name}")
except Exception as e:
    results.append(f"\033[31m{e}")
