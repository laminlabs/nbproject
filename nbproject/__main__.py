import argparse
from ._nbproject_cli import init


def main():
    parser = argparse.ArgumentParser(prog="nbproject")
    subparsers = parser.add_subparsers(help="available commands:", dest="cmd")

    parser_init = subparsers.add_parser("init", help="init the project")  # noqa: F841

    args = parser.parse_args()

    if args.cmd == "init":
        init()


if __name__ == "__main__":
    main()
