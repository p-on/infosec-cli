from __main__ import *
import httpx

try:
    response = httpx.get(f"http://ip-api.com/json/{margs[0]}?fields=17039359").json()
    results.append(f"\033[0mLocation — \033[32m{response['city']}, {response['regionName']}, {response['country']}")
    results.append(f"\033[0mCo-Ordinates — \033[32m{response['lat']}, {response['lon']}")
    results.append(f"\033[0mISP — \033[32m{response['isp']}, {response['as']}, {response['org']}")
    if response["reverse"]:
        results.append(f"\033[0mDNS — \033[32m{response['reverse']}")
    results.append(f"\033[0mMobile — \033[32m{response['mobile']}")
    results.append(f"\033[0mProxy — \033[32m{response['proxy']}")
    results.append(f"\033[0mHosting — \033[32m{response['hosting']}")
except Exception as e:
    results.append(f"\033[31m{e}")
