#!/usr/bin/env python
from pathlib import Path

from .dotfile import Status

def status(dotfile):
    if dotfile.status == Status.missing:
        print('-', dotfile.actual)

    elif dotfile.status == Status.different:
        print('!', dotfile.actual)

    elif dotfile.status == Status.symlink:
        print('S', dotfile.actual)
