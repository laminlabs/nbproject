import argparse
from pathlib import Path
from nbproject.nbproject_cli import init, sync


parser = argparse.ArgumentParser(prog="PROG")
subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")

parser_init = subparsers.add_parser("init", help="init help")

parser_sync = subparsers.add_parser("sync", help="sync help")
parser_sync.add_argument("--deps", "-d", action="store_true")
parser_sync.add_argument("--versions", "-v", action="store_true")

args = parser.parse_args()

cwd = Path.cwd()

if args.cmd == "init":
    init(cwd)
elif args.cmd == "sync":
    sync(cwd, args.deps, args.versions)
