from __main__ import *
import hashlib

try:
    results.append(hashlib.md5(margs[1].encode()).hexdigest())
except Exception as e:
    results.append(f"\033[31m{e}")