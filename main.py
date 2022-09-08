import argparse, os

parser = argparse.ArgumentParser(
    description = "a command line interface for infosec"
)

parser.add_argument("-b64", "--base64", type = str, nargs = 2,
    metavar = ("decode/encode", "string"),
    help = "modules for base64 handling"
)

args = parser.parse_args()

__all__ = [name for name in globals()]
__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")

def main():
    sargs = vars(args)

    for sarg in sargs:
        if len(sargs[sarg]) > 1:
            print(f"\033[0m[\033[32m+\033[0m] started command \033[93m{sarg}\033[0m")
            exec(open(__filepath__ + "/modules/" + sarg + "/" + sargs[sarg][0] + ".py").read())

if __name__ == "__main__": 
    main()
