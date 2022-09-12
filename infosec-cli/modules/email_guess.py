from __main__ import *
import httpx

# credit to IRIS-Team

def validate_guess(email_domain: str, domain: str) -> bool:
    if len(email_domain) != len(domain):
        return False

    positions = []
    [positions.append((position, char)) for position, char in enumerate(email_domain) if char != '*']
    for position, char in positions:
        if domain[position] != char:
            return False

    return True

try:
    if margs[0].__contains__("@"):
        margs[0] = margs[0].split("@")[1]

    if bool(re.fullmatch(DOMAIN_FORMAT, margs[0])):
        request = httpx.get("https://raw.githubusercontent.com/IRIS-Team/IRIS/main/data/domains.txt")
        email_domains = [x.strip() for x in request.text.splitlines() if len(x.strip()) > 0]
        for domain in email_domains:
            if validate_guess(str(margs[0]), domain) is True:
                results.append(str(domain))
    else:
        results.append(f"\033[31mdomain not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")
