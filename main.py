import argparse, os

parser = argparse.ArgumentParser(description="A command line interface for infosec.")
args = parser.parse_args()

__all__ = [name for name in globals()]
__filepath__ = os.path.dirname(__file__)
__dirtree__ = os.listdir(__filepath__ + "/modules")

def main():
    if args[0] != None:
        exec(open(__filepath__ + "/modules/" + args[0] + ".py").read())
        print(f"\033[0m    Loaded command module: \033[93m{args[0]}\033[0m")

if __name__ == "__main__": 
    main()
