from main import *
import hashlib

result = None

try:
    result = hashlib.md5(margs[1].encode()).hexdigest()
except Exception as e:
    result = f"\033[31m{e}"

log("*", f"\033[93m{result}")
