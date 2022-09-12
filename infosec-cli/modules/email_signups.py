from __main__ import *
import httpx, trio
from holehe.localuseragent import ua
from holehe.instruments import TrioProgress

# credit to holehe, i really cba to sort this all

def import_submodules(package, recursive=True):
    global import_submodules

    if isinstance(package, str):
        package = importlib.import_module(package)
    resultsx = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        resultsx[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            resultsx.update(import_submodules(full_name))
    return resultsx

def get_functions(modules, args=None):
    websites = []

    for module in modules:
        if len(module.split(".")) > 3 :
            modu = modules[module]
            site = module.split(".")[-1]
            if args !=None and args.nopasswordrecovery==True:
                if "adobe" not in str(modu.__dict__[site]) and "mail_ru" not in str(modu.__dict__[site]) and "odnoklassniki" not in str(modu.__dict__[site]):
                    websites.append(modu.__dict__[site])
            else:
                websites.append(modu.__dict__[site])
    return websites

async def launch_module(module, email, client, out):
    try: await module(email, client, out)
    except: pass

async def main_holehe(email, out):
    global httpx, trio, websites, modules, launch_module

    client = httpx.AsyncClient(timeout=10)
    async with trio.open_nursery() as nursery:
        for website in websites: nursery.start_soon(launch_module, website, email, client, out)
    await client.aclose()

modules = import_submodules("holehe.modules")
websites = get_functions(modules)

try:
    if bool(re.fullmatch(EMAIL_FORMAT, margs[0])):
        out = []
        trio.run(main_holehe, margs[0], out)
        for website in out:
            if website["rateLimit"] == True:
                fails.append(f"https://{website['domain']}")
                continue
            if website["exists"] == True:
                results.append(f"https://{website['domain']}")
                if website["emailrecovery"] != None:
                    results.append(f"   ↳ {website['emailrecovery']}")
                if website["phoneNumber"] != None:
                    results.append(f"   ↳ {website['phoneNumber']}")
                if website["others"] != None:
                    for other in website["others"]:
                        results.append(f"   ↳ \033[0m{other} — \033[32m{website['others'][other]}")
    else:
        results.append(f"\033[31memail not formatted properly")
except Exception as e:
    results.append(f"\033[31m{e}")
