from __main__ import *
import httpx, base64

regex_pgp = re.compile(PGP_FORMAT, re.MULTILINE)
regex_email = re.compile(EMAIL_FORMAT, re.MULTILINE)

try:
    response = httpx.get(f"https://keybase.io/{margs[0]}/pgp_keys.asc").text
    matches = regex_pgp.findall(response)
    for match in matches:
        b64 = base64.b64decode(match)
        emails = re.findall(regex_email, b64.decode("utf-8", "ignore"))
        for email in emails:
            if email not in results:
                results.append(email)
except Exception as e:
    results.append(f"\033[31m{e}")