from main import *
import base64

try:
    del margs[0]
    results.append(base64.b64decode(" ".join(margs)).decode('utf-8', 'ignore').replace('`', ' '))
except Exception as e:
    results.append(f"\033[31m{e}")
