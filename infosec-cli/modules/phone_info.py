from __main__ import *
import httpx
from bs4 import BeautifulSoup

def caller_id(number) -> None:
    global httpx

    number = number.replace("+1", "")
    number = number.lstrip("+")

    try:
        resp = httpx.post("https://api.calleridtest.com/freebie", json={"number": int("1" + number)}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})
        if resp.status_code == 200:
            resp = resp.json()
            provider = resp.get("data").get("data").get("lrn").get("company")
            city = resp.get("data").get("data").get("lrn").get("rc")
            state = resp.get("data").get("data").get("lrn").get("state_full_name")
            name = resp.get("data").get("data").get("cnam").get("name")
            return provider, city, state, name
        else:
            return "daily", "limit", "was", "reached"
    except:
        return "daily", "limit", "was", "reached"

def fone_finder(number) -> None:
    global httpx

    USANUMBER = False
    if number.__contains__("+1"): USANUMBER = True
    if not number.__contains__("+"): USANUMBER = True
    number = number.replace("+1", "")
    number = number.lstrip("+")

    if USANUMBER:
        try:
            resp = httpx.get(f"http://www.fonefinder.net/findome.php?npa={number[:3]}&nxx={number[3:6]}&thoublock={number[6:]}&usaquerytype=Search+by+Number").text
            x2 = resp.split("<TABLE border=3 cellspacing=2 cellpadding=2 BGCOLOR='#FFFFCC'><TR bgcolor='#7093DB' ALIGN=CENTER><TH>")[1].split("</A><BR></H5><center>")[0]
            city = x2.split("findcity.php?cityname=")[1].split("&")[0].replace("+", " ")
            state = x2.split("findcity.php?cityname=")[1].split("&state=")[1].split("'")[0]
            provider = x2.split("</A><TD>")[2].split("<TD>")[0].split(">")[1] + " (" + x2.split("</A><TD>")[2].split("<TD>")[0].split(".net/")[1].split(".php")[0].upper() + ")"
            return USANUMBER, city, state, provider
        except: return USANUMBER, None, None, None
    else:
        try:
            resp = httpx.get(f"http://www.fonefinder.net/findint.php?intlnum={number}&intlquery=Search+by+Number").text
            x2 = resp.split("<center><TABLE border=5 cellspacing=3 cellpadding=3>")[1].split("</CENTER><center>")[0]
            country = x2.split("FACE=arial,helvetica>")[2].split("<TD")[0]
            city = x2.split("FACE=arial,helvetica>")[3].split("<TD")[0]
            return USANUMBER, city, country, None
        except: return USANUMBER, None, None, None

def strip_phone(phone):
    phone = phone.replace("+1", "")
    phone = phone.replace("(", "")
    phone = phone.replace(")", "")
    phone = phone.replace("-", "")
    phone = phone.lstrip("1")
    return phone

try:
    if bool(re.fullmatch(PHONE_FORMAT, margs[0])):
        USA, cityf, countryf, providerf = fone_finder(margs[0])
        if not USA:
            if cityf or countryf:
                results.append(f"\033[0mLocation — \033[32m{cityf}, {countryf}")
            if providerf:
                results.append(f"\033[0mProvider — \033[32m{providerf}")
        else:
            margs[0] = strip_phone(margs[0])
            response = httpx.get(f"https://www.canada411.ca/search/?stype=re&what=%28{margs[0][:3]}%29+{margs[0][3:6]}-{margs[0][6:]}").text
            soup = BeautifulSoup(response, "html.parser")
            name = soup.find("h1", attrs={"class": "vcard__name"})
            addy = soup.find("div", attrs={"class": "c411Address vcard__address"})

            if addy:
                results.append(f"\033[0mLocation — \033[32m{addy}")
            if name:
                results.append(f"\033[0mName — \033[32m{name}")
            if not name and not addy:
                provider, city, state, name = caller_id(margs[0])
                if provider != "daily":
                    if city or state:
                        results.append(f"\033[0mLocation — \033[32m{city}, {state}")
                    elif cityf or countryf:
                        results.append(f"\033[0mLocation — \033[32m{cityf}, {countryf}")
                    if name:
                        results.append(f"\033[0mName — \033[32m{name}")
                else:
                    results.append("\033[31mhttps://calleridtest.com/ limit reached, or not connected to USA proxy (maybe try visiting the site?), falling back to http://fonefinder.net/")
                    if cityf or countryf:
                        results.append(f"\033[0mLocation — \033[32m{cityf}, {countryf}")
            if provider and provider != "daily":
                results.append(f"\033[0mProvider — \033[32m{provider}")
            elif providerf:
                results.append(f"\033[0mProvider — \033[32m{providerf}")
    else:
        results.append(f"\033[31mphone not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")

# this code needs to be better (pls)