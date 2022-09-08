import argparse, os, json

__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")
__settings__ = json.load(open(__filepath__ + "/settings.json"))

def __validate_guess__(email_domain: str, domain: str) -> bool:
    if len(email_domain) != len(domain):
        return False
    
    positions = []
    [positions.append((position, char)) for position, char in enumerate(email_domain) if char != '*']
    for position, char in positions:
        if domain[position] != char:
            return False

    return True

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

    args = parser.parse_args()
    sargs = vars(args)

    for sarg in sargs:
        margs = sargs[sarg]
        __all__ = [name for name in globals()]

        if margs != None:
            print(f"\033[0m[\033[32m+\033[0m] started command \033[93m{sarg}\033[0m")
            try:
                exec(open(__filepath__ + "/modules/" + sarg + "/" + margs[0] + ".py").read())
            except Exception as e:
                print(e)

if __name__ == "__main__": 
    main()
