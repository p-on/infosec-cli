from main import *
import base64

try:
    del margs[0]
    results.append(base64.b64encode(" ".join(margs).encode()).decode('utf-8', 'ignore'))
except Exception as e:
    results.append(f"\033[31m{e}")
