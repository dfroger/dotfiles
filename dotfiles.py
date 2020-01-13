#!/usr/bin/env python

from pathlib import Path
import logging
import argparse
import json
from enum import Enum
import shutil
from collections import defaultdict
from typing import Dict, List
import subprocess

logger = logging.getLogger()


class Status(Enum):
    OK = 1
    NOT_INSTALLED = 2
    DIFFERENT = 3
    SYMLINK = 4
    NOT_BACKED_UP = 5


def dotted(p: Path) -> Path:
    return Path(str(p).replace("_", ".", 1)) if str(p).startswith("_") else p


def underscored(p: Path) -> Path:
    return Path(str(p).replace(".", "_", 1)) if str(p).startswith(".") else p


class DotFile:
    def __init__(self, backup_dir: Path, backup: Path, install_dir: Path):
        self.backup_dir = backup_dir
        self.backup = backup

        self.actual_relative = dotted(backup.relative_to(backup_dir))

        self.actual = install_dir / self.actual_relative
        self.status = self._compute_status()

    def _compute_status(self):
        if not self.actual.exists():
            return Status.NOT_INSTALLED

        if not self.backup.exists():
            return Status.NOT_BACKED_UP

        if self.actual.is_symlink():
            return Status.SYMLINK

        with self.backup.open() as f:
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
    parser.add_argument(
        "--install-dir", "-i", type=Path, default=Path.home(), help="Path to the installation directory",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
    parser.add_argument(
        "--no-action",
        "-n",
        action="store_true",
        help="Do not actually do anything, just log action",
    )
    subparsers = parser.add_subparsers()

    parser_status = subparsers.add_parser(
        "status", help="List statuses of the dot files"
    )
    parser_status.add_argument(
        "--hide-ok",
        action="store_true",
        help="Do not report dot files with up-to-dated backup",
    )
    parser_status.set_defaults(func=cmd_status)

    parser_install = subparsers.add_parser("install", help="Install the dot files")
    parser_install.set_defaults(func=cmd_install)

    parser_backup = subparsers.add_parser("backup", help="Backup the dot files")
    parser_backup.set_defaults(func=cmd_backup)

    args = parser.parse_args(argv)
    return args


def read_conf(path: Path) -> Dict:
    if path.is_file():
        logger.debug(f"Read config file: {path}")
        with path.open() as f:
            data = json.load(f)
        return {"backup": [Path(p) for p in data["backup"]]}
    else:
        raise FileNotFoundError(f"Missing config file: {path}")


def find_dotfiles(backup_dirs: List[Path], install_dir: Path) -> List[DotFile]:
    dotfiles = []
    for backup_dir in backup_dirs:
        for backup in backup_dir.glob("**/*"):
            if backup.is_dir():
                continue
            dotfiles.append(DotFile(backup_dir, backup, install_dir))

    # Check is there are files in ~/bin that are not backed up
    bindir = install_dir / "bin"
    for p in bindir.iterdir():
        if p.is_dir():
            pass
        r = p.relative_to(bindir)
        u = underscored(r)
        for backup_dir in backup_dirs:
            if (backup_dir / "bin" / u).exists():
                break
        else:
            dotfiles.append(DotFile(backup_dirs[0], backup_dirs[0] / "bin" / u, install_dir))
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
            if dotfile.status in (Status.OK, Status.SYMLINK):
                if not args.hide_ok:
                    line(" ", dotfile)

            elif dotfile.status == Status.NOT_INSTALLED:
                line("∅", dotfile)

            elif dotfile.status == Status.DIFFERENT:
                line("≠", dotfile)

            elif dotfile.status == Status.NOT_BACKED_UP:
                line("⚠️", dotfile)

            else:
                raise ValueError(f"Unexpected status: {dotfile.status}")

        print()


def cmd_install(dotfiles: List[DotFile], args):
    action = not args.no_action

    for dotfile in dotfiles:
        logger.debug(f"Installing {dotfile.actual_relative}")

        if dotfile.status == Status.OK:
            logger.debug(f"{dotfile.actual} is already installed")
            continue

        elif dotfile.status == Status.NOT_INSTALLED:
            directory = dotfile.actual.parent
            if not directory.is_dir():
                print(f"mkdir -p {directory}")
                if action:
                    directory.mkdir(parents=True)

            print(f"cp {dotfile.backup} {dotfile.actual}")
            print()
            if action:
                shutil.copy(str(dotfile.backup), str(dotfile.actual))


def cmd_backup(dotfiles: List[DotFile], args):
    for dotfile in dotfiles:
        if dotfile.status in (Status.DIFFERENT, Status.NOT_BACKED_UP):
            subprocess.run(
                ["/usr/local/bin/nvim", "-d", dotfile.actual, dotfile.backup]
            )


def main():
    args = parse_command_line()
    configure_logger(args.verbose)
    conf = read_conf(args.config)
    backup_dirs = conf["backup"] if args.backup is None else args.backup
    dotfiles = find_dotfiles(backup_dirs, args.install_dir)

    args.func(dotfiles, args)


if __name__ == "__main__":
    main()
