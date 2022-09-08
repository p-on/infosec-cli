from main import *

result = None

try:
    hashfile = open(__settings__["hash_files"] + margs[1][:2] + "/" + margs[1][2:4] + ".txt", encoding="latin-1")
    hashes = hashfile.read().splitlines()
    for hash in hashes:
        if hash.__contains__(margs[1] + ":"): 
            result = hash.split(":")[1]
except Exception as e:
    result = f"\033[31m{e}"

log("*", f"\033[93m{result}")
