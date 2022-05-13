import argparse
from ._nbproject_cli import init, sync


def main():
    parser = argparse.ArgumentParser(prog="nbproject")
    subparsers = parser.add_subparsers(help="available commands:", dest="cmd")

    parser_init = subparsers.add_parser("init", help="init the project")  # noqa: F841

    parser_sync = subparsers.add_parser(
        "sync", help="synchronize the notebooks of the project"
    )
    parser_sync.add_argument(
        "files_dirs", nargs="+", help="which files and folders to synchronize"
    )
    parser_sync.add_argument(
        "--deps",
        "-d",
        action="store_true",
        help="parse dependencies from the notebooks",
    )
    parser_sync.add_argument(
        "--versions",
        "-v",
        action="store_true",
        help="also pin the versions from the current environment",
    )

    args = parser.parse_args()

    if args.cmd == "init":
        init()
    elif args.cmd == "sync":
        sync(args.files_dirs, args.deps, args.versions)


if __name__ == "__main__":
    main()
