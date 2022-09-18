import argparse, os, json, re, threading, pkgutil, importlib, sys, math

__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")
__settings__ = json.load(open(__filepath__ + "/__settings__.json"))

EMAIL_FORMAT = r'\b[A-Za-z0-9*._%+-]+@[A-Za-z0-9*.-]+\.[A-Z*|a-z*]{2,}\b'
DOMAIN_FORMAT = r'\b[A-Za-z0-9*_-]+\.[A-Z*|a-z*]{2,}\b'
DOMAINSHORT_FORMAT = r'\b[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_\/]+'
PGP_FORMAT = r"(?=\n([A-Za-z0-9+\/=\s][^:-]+)\n)|(?=^\s)"
PHONE_FORMAT = re.compile(r"\+?([0-9]{0,3})\d?([0-9]{3})-?([0-9]{3})-?([0-9]{4})", re.UNICODE)
DISCORD_FORMAT = r'(.{2,32}([^a-zA-Z0-9_\-\/()\[\]{}])\d{4})'

def log(to: str, what: str):
    if to == "*": to = "\033[93m*"
    if to == "+": to = "\033[32m+"
    if to == "-": to = "\033[31m-"

    print(f"\033[0m[{to}\033[0m] {what}\033[0m")

def sort_out(string):
    return "_".join(string.casefold().split())

def main() -> None:
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.prog = "infosec-cli"
    parser.description = "a suite of tools condensed into a python cli to facilitate the collection and analysis of data gathered from open sources for intelligence"
    parser.epilog = "pigeon & 7ap were here"

    parser.add_argument("-f", "--fails",
        action = "store_true",
        help = "show fails for the specific command"
    )
    parser.add_argument("-b64-e", "--b64-encode",
        nargs = "+", type = str,
        default = argparse.SUPPRESS,
        help = "encodes string to base64"
    )
    parser.add_argument("-b64-d", "--b64-decode",
        nargs = "+", type = str,
        default = argparse.SUPPRESS,
        help = "decodes base64 to string"
    )
    parser.add_argument("-md5-h", "--md5-hash",
        nargs = "+", type = str,
        default = argparse.SUPPRESS,
        help = "hashes string to md5"
    )
    parser.add_argument("-md5-d", "--md5-dehash",
        nargs = "+", type = str,
        default = argparse.SUPPRESS,
        help = "dehashes md5 to string"
    )
    parser.add_argument("-em-g", "--email-guess",
        nargs = 1, type = str, metavar = "email",
        default = argparse.SUPPRESS,
        help = "attempts to guess email based on * characters"
    )
    parser.add_argument("-em-s", "--email-signups",
        nargs = 1, type = str, metavar = "email",
        default = argparse.SUPPRESS,
        help = "checks sites the email has signed up to"
    )
    parser.add_argument("-un-s", "--username-signups",
        nargs = 1, type = str, metavar = "username",
        default = argparse.SUPPRESS,
        help = "checks sites the username has signed up to"
    )
    parser.add_argument("-dm-i", "--domain-info",
        nargs = 1, type = str, metavar = "domain",
        default = argparse.SUPPRESS,
        help = "looks for info on the domain"
    )
    parser.add_argument("-dm-s", "--domain-sub",
        nargs = 1, type = str, metavar = "domain",
        default = argparse.SUPPRESS,
        help = "looks for subdomains on the domain"
    )
    parser.add_argument("-ip-i", "--ip-info",
        nargs = 1, type = str, metavar = "ip",
        default = argparse.SUPPRESS,
        help = "looks for info on the ip"
    )
    parser.add_argument("-ph-i", "--phone-info",
        nargs = 1, type = str, metavar = "phone",
        default = argparse.SUPPRESS,
        help = "looks for info on the phone"
    )
    parser.add_argument("-gh-l", "--github-leaks",
        nargs = 1, type = str, metavar = "github username",
        default = argparse.SUPPRESS,
        help = "searches for email leakage on github"
    )
    parser.add_argument("-kb-l", "--keybase-leaks",
        nargs = 1, type = str, metavar = "keybase username",
        default = argparse.SUPPRESS,
        help = "searches for email leakage on keybase"
    )
    parser.add_argument("-kb-i", "--keybase-info",
        nargs = 1, type = str, metavar = "keybase username",
        default = argparse.SUPPRESS,
        help = "searches for info on keybase username"
    )
    parser.add_argument("-gh-i", "--github-info",
        nargs = 1, type = str, metavar = "github username",
        default = argparse.SUPPRESS,
        help = "searches for info on github username"
    )
    parser.add_argument("-tw-i", "--twitch-info",
        nargs = 1, type = str, metavar = "twitch username",
        default = argparse.SUPPRESS,
        help = "searches for info on twitch username"
    )
    parser.add_argument("-gd-i", "--googledocs-info",
        nargs = 1, type = str, metavar = "doc link",
        default = argparse.SUPPRESS,
        help = "searches for info (including owner info) on google document"
    )
    parser.add_argument("-rb-i", "--roblox-info",
        nargs = "+", type = str, metavar = "roblox username",
        default = argparse.SUPPRESS,
        help = "searches for info on roblox username"
    )
    # parser.add_argument( ... )

    args = parser.parse_args()
    sargs = vars(args)

    results, fails = [], []

    for sarg in sargs: # apologies for shitty argparse handling here, semi-argparse system in place, if this is out in release then it may be cleaned in the future // TODO: *please* learn argparse
        margs = sargs[sarg]
        __all__ = [name for name in globals()]

        if type(margs) == list and margs != None:
            log("*", f"started command \033[93m{sarg}")
            try:
                exec(open(__filepath__ + "/modules/" + sort_out(sarg) + ".py").read())
            except Exception as e:
                print(e)

    for result in results:
        log("+", f"\033[32m{result}")
    if args.fails:
        for result in fails:
            log("-", f"\033[31m{result}")

if __name__ == "__main__":
    main()
