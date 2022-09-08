import argparse, os, json, re, threading, pkgutil, importlib, sys

__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")
__settings__ = json.load(open(__filepath__ + "/settings.json"))

EMAIL_FORMAT = r'\b[A-Za-z0-9*._%+-]+@[A-Za-z0-9*.-]+\.[A-Z*|a-z*]{2,}\b'
DOMAIN_FORMAT = r'\b[A-Za-z0-9*_-]+\.[A-Z*|a-z*]{2,}\b'
DOMAINSHORT_FORMAT = r'\b[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_\/]+'
PGP_FORMAT = r"(?=\n([A-Za-z0-9+\/=\s][^:-]+)\n)|(?=^\s)"

def log(to: str, what: str):
    if to == "*": to = "\033[93m*"
    elif to == "+": to = "\033[32m+"
    elif to == "-": to = "\033[31m-"

    print(f"\033[0m[{to}\033[0m] {what}\033[0m")

def main():
    results, fails = [], []

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
        metavar = ("guess/signups", "email"),
        help = "modules for email int"
    ) # email command, no more to say

    parser.add_argument("-f", "--fails", action="store_true",
        help = "show fails if any occur in given command"
    )

    args = parser.parse_args()
    sargs = vars(args)

    for sarg in sargs: # apologies for shitty argparse handling here, semi-argparse system in place, if this is out in release then it may be cleaned in the future // TODO: *please* learn argparse
        margs = sargs[sarg]
        __all__ = [name for name in globals()]

        if type(margs) == list and margs != None:
            log("*", f"started command \033[93m{sarg} {margs[0]}")
            try:
                exec(open(__filepath__ + "/modules/" + sarg + "/" + margs[0] + ".py").read())
            except Exception as e:
                print(e)

    for result in results:
        log("+", f"\033[32m{result}")
    if args.fails:
        for result in fails:
            log("-", f"\033[31m{result}")

if __name__ == "__main__": 
    main()
