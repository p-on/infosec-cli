from main import *
import httpx, trio
from holehe.localuseragent import ua
from holehe.instruments import TrioProgress

# credit to holehe, i really cba to sort this all

async def main_holehe(email, out):
    global httpx, trio, websites, modules
    
    client = httpx.AsyncClient(timeout=10)
    async with trio.open_nursery() as nursery:
        for website in websites: nursery.start_soon(launch_module, website, email, client, out)
    await client.aclose()

modules = import_submodules("holehe.modules")
websites = get_functions(modules)

try:
    if bool(re.fullmatch(EMAIL_FORMAT, margs[1])):
        out = []
        trio.run(main_holehe, margs[1], out)
        for website in out:
            if website["rateLimit"] == True:
                fails.append(f"https://{website['domain']}")
                continue
            if website["exists"] == True:
                results.append(f"https://{website['domain']}")
    else:
        results.append(f"\033[31memail not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")
