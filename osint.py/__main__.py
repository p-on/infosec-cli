import argparse

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.prog = "osint.py"
    parser.description = "A suite of tools condensed into a Python script to facilitate the collection and analysis of data gathered from open sources to produce actionable intelligence."
    parser.epilog = "pigeon & 7ap were here!"

    # parser.add_argument( ... )
    # parser.add_argument( ... )
    # parser.add_argument( ... )

    args = parser.parse_args()

if __name__ == "__main__":
    main()
