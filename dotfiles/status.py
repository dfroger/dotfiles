#!/usr/bin/env python
from pathlib import Path

from .dotfile import Status

def status(dotfile):
    if dotfile.status == Status.dont_exist:
        print('!', dotfile.installed)

    elif dotfile.status == Status.not_symlink:
        print('?', dotfile.installed)

    elif dotfile.status == Status.wrong_symlink:
        print('B', dotfile.installed)

    elif dotfile.status == Status.to_merge:
        print('G', dotfile.installed)
