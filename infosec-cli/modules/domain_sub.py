from __main__ import *
import httpx

try:
    if bool(re.fullmatch(DOMAIN_FORMAT, margs[0])):
        try:
            response = httpx.get(f"https://crt.sh/?q={margs[0]}").content
            links = re.compile("<TD>(.*?)</TD>").findall(str(response))
            for item in links:
                subdomains = []
                item = item.strip()
                if "<BR>" in item: 
                    subdomains = item.split("<BR>")
                else:
                    subdomains.append(item)
                for subdomain in subdomains:
                    subdomain = subdomain.strip()
                    if not subdomain.endswith("." + margs[0]):
                        continue
                    if not subdomain in results:
                        results.append(subdomain)
        except: pass
        try:
            response = httpx.get(f"https://api.sublist3r.com/search.php?domain={margs[0]}").json()
            for item in response:
                if not item in results:
                    results.append(item)
        except: pass
        try:
            response = httpx.get(f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={margs[0]}").json()["subdomains"]
            for item in response:
                if not item in results:
                    results.append(item)
        except Exception as e: print(e)
    else:
        results.append(f"\033[31mdomain not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")