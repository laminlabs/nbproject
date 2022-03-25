import argparse
from nbproject._nbproject_cli import init, sync


parser = argparse.ArgumentParser(prog="PROG")
subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")

parser_init = subparsers.add_parser("init", help="init help")

parser_sync = subparsers.add_parser("sync", help="sync help")
parser_sync.add_argument("files_dirs", nargs="+", help="paths help")
parser_sync.add_argument("--deps", "-d", action="store_true")
parser_sync.add_argument("--versions", "-v", action="store_true")

args = parser.parse_args()

if args.cmd == "init":
    init()
elif args.cmd == "sync":
    sync(args.files_dirs, args.deps, args.versions)
