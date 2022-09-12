from __main__ import *
import httpx

try:
    response = httpx.get(f"https://api.github.com/users/{margs[0]}/events?per_page=100").json()
    for data in response:
        try:
            for info in data["payload"]["commits"]:
                if not info["author"]["email"] in results:
                    results.append(info["author"]["email"])
        except: pass
except Exception as e:
    results.append(f"\033[31m{e}")
