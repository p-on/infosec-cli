from main import *
import base64

result = None

try:
    result = base64.b64decode(margs[1]).decode('utf-8', 'ignore').replace('`', ' ')
except Exception as e:
    result = f"\033[31m{e}"

log("*", f"\033[93m{result}")
