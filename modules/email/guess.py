from main import *
import requests

# credit to IRIS-Team

results = []

try:
    if margs[1].__contains__("@"): 
        margs[1] = margs[1].split("@")[1]

    with requests.get("https://raw.githubusercontent.com/IRIS-Team/IRIS/main/data/domains.txt") as request:
        email_domains = [x.strip() for x in request.text.splitlines() if len(x.strip()) > 0]
        for domain in email_domains:
            if __validate_guess__(str(margs[1]), domain) is True:
                results.append(str(domain))
except Exception as e:
    results = [f"\033[31m{e}"]

for result in results:
    log("*", f"\033[93m{result}")
