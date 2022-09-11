from __main__ import *
import httpx
from datetime import datetime

try:
    response = httpx.get(f"https://keybase.io/_/api/1.0/user/lookup.json?usernames={margs[0]}").json()
    them = response["them"][0]
    if them["profile"]["full_name"]:
        results.append(f"\033[0mFull Name — \033[32m{them['profile']['full_name']}")
    if them["profile"]["location"]:
        results.append(f"\033[0mLocation — \033[32m{them['profile']['location']}")
    if them["profile"]["bio"]:
        results.append(f"\033[0mBio — \033[32m{them['profile']['bio']}")
    if them["basics"]["ctime"]:
        results.append(f"\033[0mCreated — \033[32m{datetime.fromtimestamp(them['basics']['ctime'])}")
    if them["basics"]["last_id_change"] > them["basics"]["mtime"]:
        results.append(f"\033[0mLast Updated — \033[32m{datetime.fromtimestamp(them['basics']['last_id_change'])}")
    else:
        results.append(f"\033[0mLast Updated — \033[32m{datetime.fromtimestamp(them['basics']['mtime'])}")
    for sig in them["proofs_summary"]["all"]:
        results.append(f"\033[0m{sig['proof_type'][:1].upper()}{sig['proof_type'][1:]} Link — \033[32m{sig['service_url']}")
        results.append(f"   ↳ \033[0mProof — \033[32m{sig['proof_url']}")
    for sig in them["cryptocurrency_addresses"]:
        for lsig in them["cryptocurrency_addresses"][sig]:
            results.append(f"\033[0m{sig[:1].upper()}{sig[1:]} Address — \033[32m{lsig['address']}")
    for sig in them["devices"]:
        sig = them["devices"][sig]
        results.append(f"\033[0m{sig['type'][:1].upper()}{sig['type'][1:]} Device — \033[32m{sig['name']}")
except Exception as e:
    results.append(f"\033[31m{e}")