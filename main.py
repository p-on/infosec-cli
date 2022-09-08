import argparse, os, json, re, threading, pkgutil, importlib, sys

__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")
__settings__ = json.load(open(__filepath__ + "/settings.json"))

EMAIL_FORMAT = r'\b[A-Za-z0-9*._%+-]+@[A-Za-z0-9*.-]+\.[A-Z*|a-z*]{2,}\b'
DOMAIN_FORMAT = r'\b[A-Za-z0-9*_-]+\.[A-Z*|a-z*]{2,}\b'
DOMAINSHORT_FORMAT = r'\b[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_\/]+'
PGP_FORMAT = r"(?=\n([A-Za-z0-9+\/=\s][^:-]+)\n)|(?=^\s)"

def __validate_guess__(email_domain: str, domain: str) -> bool:
    if len(email_domain) != len(domain):
        return False
    
    positions = []
    [positions.append((position, char)) for position, char in enumerate(email_domain) if char != '*']
    for position, char in positions:
        if domain[position] != char:
            return False

    return True

def import_submodules(package, recursive=True):
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
                if  "adobe" not in str(modu.__dict__[site]) and "mail_ru" not in str(modu.__dict__[site]) and "odnoklassniki" not in str(modu.__dict__[site]):
                    websites.append(modu.__dict__[site])
            else:
                websites.append(modu.__dict__[site])
    return websites

async def launch_module(module, email, client, out):
    try: await module(email, client, out)
    except: pass

def log(to: str, what: str):
    if to == "*": to = "\033[93m*"
    elif to == "+": to = "\033[32m+"
    elif to == "-": to = "\033[31m-"

    print(f"\033[0m[{to}\033[0m] {what}\033[0m")

def main():
    parser = argparse.ArgumentParser(
        description = "a command line interface for infosec"
    )

    parser.add_argument("-b64", "--base64", type = str, nargs = "*",
        metavar = ("decode/encode", "string"),
        help = "modules for base64 handling"
    ) # base64 command for testing purposes

    parser.add_argument("-md5", type = str, nargs = 2,
        metavar = ("dehash/hash", "string"),
        help = "modules for md5 handling"
    ) # md5 command for further testing purposes, hash_files must be configured properly and formatted properly before running dehash

    parser.add_argument("-em", "--email", type = str, nargs = 2,
        metavar = ("guess", "email"),
        help = "modules for email int"
    ) # email command, no more to say

    parser.add_argument("-f", "--fails", action="store_true",
        help = "show fails if any occur in given command"
    )

    args = parser.parse_args()
    sargs = vars(args)

    for sarg in sargs:
        margs = sargs[sarg]
        __all__ = [name for name in globals()]

        if type(margs) == list and margs != None:
            print(f"\033[0m[\033[32m+\033[0m] started command \033[93m{sarg}\033[0m")
            try:
                exec(open(__filepath__ + "/modules/" + sarg + "/" + margs[0] + ".py").read())
            except Exception as e:
                print(e)

if __name__ == "__main__": 
    main()
