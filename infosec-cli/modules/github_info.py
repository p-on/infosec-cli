from __main__ import *
import httpx
import dateutil.parser as dp

def to_readable(string):
    global dp

    stamp = dp.parse(string)
    return stamp

try:
    response = httpx.get(f"https://api.github.com/users/{margs[0]}").json()
    if response["name"]:
        results.append(f"\033[0mName — \033[32m{response['name']}")
    if response["company"]:
        results.append(f"\033[0mCompany — \033[32mhttps://github.com/{response['company']}")
    if response["blog"]:
        results.append(f"\033[0mBlog — \033[32m{response['blog']}")
    if response["location"]:
        results.append(f"\033[0mLocation — \033[32m{response['location']}")
    if response["email"]:
        results.append(f"\033[0mEmail — \033[32m{response['email']}")
    if response["bio"]:
        results.append(f"\033[0mBio — \033[32m{response['bio']}")
    if response["twitter_username"]:
        results.append(f"\033[0mTwitter Link — \033[32mhttps://twitter.com/{response['twitter_username']}")
    results.append(f"\033[0mCreated — \033[32m{to_readable(response['created_at'])}")
    results.append(f"\033[0mLast Updated — \033[32m{to_readable(response['updated_at'])}")
except Exception as e:
    results.append(f"\033[31m{e}")