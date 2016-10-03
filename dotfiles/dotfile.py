#!/usr/bin/env python
from logging import getLogger
from pathlib import Path
from enum import Enum
import os

logger = getLogger('dotfiles.dotfile')

class Status(Enum):
    ok = 1
    missing = 2
    different = 3
    symlink = 4

class DotFile:

    def __init__(self, dotfiles_dir, dotfile):
        self.dotfiles_dir = dotfiles_dir
        self.dotfile = dotfile
        self.relative_path = dotfile.relative_to(dotfiles_dir)
        self.actual = self._compute_actual()
        self.status = self._compute_status()

    def _compute_actual(self):
        if str(self.relative_path).startswith('_'):
            self.relative_path = str(self.relative_path).replace('_', '.', 1)
        return Path.home() / self.relative_path

    def _compute_status(self):
        if not self.actual.exists():
            return Status.missing

        if self.actual.is_symlink():
            return Status.symlink

        with self.dotfile.open() as f:
            dotfile_content = f.read().strip()

        with self.actual.open() as f:
            actual_content = f.read().strip()

        if dotfile_content != actual_content:
            return Status.different

        return Status.ok

def find_dotfiles(dotfiles_dir):
    dotfiles = []
    for dotfile in dotfiles_dir.glob('**/*'):
        if dotfile.is_dir():
            continue
        dotfiles.append(DotFile(dotfiles_dir, dotfile))
    return dotfiles
