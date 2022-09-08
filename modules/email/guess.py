from main import *
import httpx

# credit to IRIS-Team

try:
    if margs[1].__contains__("@"): 
        margs[1] = margs[1].split("@")[1]

    if bool(re.fullmatch(DOMAIN_FORMAT, margs[1])):
        request = httpx.get("https://raw.githubusercontent.com/IRIS-Team/IRIS/main/data/domains.txt")
        email_domains = [x.strip() for x in request.text.splitlines() if len(x.strip()) > 0]
        for domain in email_domains:
            if __validate_guess__(str(margs[1]), domain) is True:
                results.append(str(domain))
    else:
        results.append(f"\033[31mdomain not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")
