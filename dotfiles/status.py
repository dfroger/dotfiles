#!/usr/bin/env python
from pathlib import Path
from collections import defaultdict

from .dotfile import Status

def line(symbol, dotfile):
    print(symbol, dotfile.relative_path)


def status(dotfiles):
    by_dotfiles_dir = defaultdict(list)

    for dotfile in dotfiles:
        by_dotfiles_dir[dotfile.dotfiles_dir].append(dotfile)

    for dotfiles_dir, dotfiles in by_dotfiles_dir.items():

        print("="*60)
        print(dotfiles_dir)
        print()

        for dotfile in dotfiles:
            if dotfile.status == Status.missing:
                line('-', dotfile)

            elif dotfile.status == Status.different:
                line('!', dotfile)

            elif dotfile.status == Status.symlink:
                line('S', dotfile)

        print()
