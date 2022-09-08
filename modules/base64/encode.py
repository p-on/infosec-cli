from main import *
import base64

result = None

try:
    result = base64.b64encode(margs[1].encode()).decode('utf-8', 'ignore')
except Exception as e:
    result = f"\033[31m{e}"

log("*", f"\033[93m{result}")
