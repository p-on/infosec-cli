from __main__ import *

try:
    hashfile = open(__settings__["hash_files"] + margs[0][:2] + "/" + margs[0][2:4] + ".txt", encoding="latin-1")
    hashes = hashfile.read().splitlines()
    for hash in hashes:
        if hash.__contains__(margs[0] + ":"): 
            results.append(hash.split(":")[1])
except Exception as e:
    results.append(f"\033[31m{e}")