from __main__ import *
import base64

try:
    results.append(base64.b64decode(" ".join(margs)).decode('utf-8', 'ignore').replace('`', ' '))
except Exception as e:
    results.append(f"\033[31m{e}")
