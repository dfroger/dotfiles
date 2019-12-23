#!/usr/bin/env python

from pathlib import Path
import logging
import argparse
import json
from enum import Enum
import shutil
from collections import defaultdict
from typing import Dict, List

logger = logging.getLogger()


class Status(Enum):
    OK = 1
    MISSING = 2
    DIFFERENT = 3
    SYMLINK = 4


class DotFile:
    def __init__(self, backup_dir: Path, dotfile: Path):
        self.backup_dir = backup_dir
        self.dotfile = dotfile

        self.actual_relative = dotfile.relative_to(backup_dir)
        if str(self.actual_relative).startswith("_"):
            self.actual_relative = Path(str(self.actual_relative).replace("_", ".", 1))

        self.actual = Path.home() / self.actual_relative
        self.status = self._compute_status()

    def _compute_status(self):
        if not self.actual.exists():
            return Status.MISSING

        if self.actual.is_symlink():
            return Status.SYMLINK

        with self.dotfile.open() as f:
            dotfile_content = f.read().strip()

        with self.actual.open() as f:
            actual_content = f.read().strip()

        if dotfile_content != actual_content:
            return Status.DIFFERENT

        return Status.OK


def parse_command_line(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        default=Path.home() / ".config" / "dotfiles" / "config.json",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--backup", "-b", nargs="+", type=Path, help="Path to the backup directories",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
    parser.add_argument(
        "--no-action",
        "-n",
        action="store_true",
        help="Do not actually do anything, just log action",
    )
    subparsers = parser.add_subparsers()

    parser_install = subparsers.add_parser("install", help="Install the dot files")
    parser_install.set_defaults(func=cmd_install)

    parser_status = subparsers.add_parser(
        "status", help="List statuses of the dot files"
    )
    parser_status.set_defaults(func=cmd_status)

    args = parser.parse_args(argv)
    return args


def read_conf(path: Path) -> Dict:
    if path.is_file():
        logger.debug(f"Read config file: {path}")
        with path.open() as f:
            data = json.load(f)
        return {"backup": [Path(p) for p in data["backup"]]}
    else:
        raise FileNotFoundError("Missing config file: {path}")


def find_dotfiles(backup_dirs: List[Path]) -> List[DotFile]:
    dotfiles = []
    for backup_dir in backup_dirs:
        for dotfile in backup_dir.glob("**/*"):
            if dotfile.is_dir():
                continue
            dotfiles.append(DotFile(backup_dir, dotfile))
    return dotfiles


def configure_logger(verbose: bool):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    formatter = logging.Formatter(fmt="%(name)-16s: %(levelname)-8s: %(message)s",)

    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(level)

    logger = logging.getLogger("dotfiles")
    logger.addHandler(consolehandler)
    logger.setLevel(level)


def line(symbol, dotfile):
    print(symbol, dotfile.actual_relative)


def cmd_status(dotfiles: List[DotFile], args):
    by_backup_dirs: Dict[Path, List[DotFile]] = defaultdict(list)

    for dotfile in dotfiles:
        by_backup_dirs[dotfile.backup_dir].append(dotfile)

    for backup_dir, dotfiles in by_backup_dirs.items():

        print("=" * 60)
        print(backup_dir)
        print()

        for dotfile in dotfiles:
            if dotfile.status == Status.MISSING:
                line("-", dotfile)

            elif dotfile.status == Status.DIFFERENT:
                line("!", dotfile)

            elif dotfile.status == Status.SYMLINK:
                line("S", dotfile)

        print()


def cmd_install(dotfiles: List[DotFile], args):

    action = not args.no_action

    for dotfile in dotfiles:
        logger.debug("Installing {}".format(dotfile.actual_relative))

        if dotfile.status == Status.OK:
            logger.debug("{} is already installed".format(dotfile.actual))
            return

        elif dotfile.status == Status.MISSING:
            directory = dotfile.actual.parent
            if not directory.is_dir():
                print("mkdir -p {}".format(directory))
                if action:
                    directory.mkdir(parents=True)

            print("cp {} {}".format(str(dotfile.dotfile), str(dotfile.actual)))
            print()
            if action:
                shutil.copy(str(dotfile.dotfile), str(dotfile.actual))


def main():
    args = parse_command_line()
    configure_logger(args.verbose)
    conf = read_conf(args.config)
    backup_dirs = conf["backup"] if args.backup is None else args.backup
    dotfiles = find_dotfiles(backup_dirs)

    args.func(dotfiles, args)


if __name__ == "__main__":
    main()
