from __main__ import *
import httpx

try:
    if bool(re.fullmatch(DOMAIN_FORMAT, margs[0])):
        response = httpx.get(f"http://ip-api.com/json/{margs[0]}?fields=17039359").json()
        ip = response["query"]
        results.append(f"\033[0mIP — \033[32m{ip}")
        response2 = httpx.get(f"https://api.bgpview.io/ip/{ip}").json()["data"]
        if response2["iana_assignment"]["whois_server"]:
            results.append(f"\033[0mWhois Server — \033[32m{response2['iana_assignment']['whois_server']}")
        if len(response2["prefixes"]) > 0:
            for prefix in response2["prefixes"]:
                results.append(f"\033[0mPrefix — \033[32m{prefix['ip']} ({prefix['cidr']}) — {prefix['asn']['asn']} {prefix['asn']['name']}/{prefix['name']} {prefix['asn']['description']}/{prefix['description']}")
        results.append(f"\033[0mLocation — \033[32m{response['city']}, {response['regionName']}, {response['country']}")
        results.append(f"\033[0mCo-Ordinates — \033[32m{response['lat']}, {response['lon']}")
        results.append(f"\033[0mISP — \033[32m{response['isp']}, {response['as']}, {response['org']}")
        if response["reverse"]:
            results.append(f"\033[0mDNS — \033[32m{response['reverse']}")
    else:
        results.append(f"\033[31mdomain not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")