#!/usr/bin/env python
from logging import getLogger
from pathlib import Path
from enum import Enum
import os

logger = getLogger('dotfiles.dotfile')

class Status(Enum):
    ok = 1
    dont_exist = 2
    not_symlink = 3
    wrong_symlink = 4
    to_merge = 5

class DotFile:

    def __init__(self, context, source_relative):
        self.context = context
        self.source_relative = source_relative
        self.source = (context.source_dir / source_relative).resolve()
        self.installed = self._compute_actual()
        self.installed_backup = Path(str(self.installed) + '.tomerge')
        self.status = self._compute_status()

    def symlink(self):
        parent = self.installed.parent
        logger.info('Installing {}'.format(self.installed))
        if self.context.no_action:
            return
        if not parent.is_dir():
            os.makedirs(str(parent))
        self.installed.symlink_to(self.source)

    def backup(self):
        logger.info('Backing up {} in {}'.
            format(self.installed, self.installed_backup))
                                                 
        if self.context.no_action:
            return True

        try:
            self.installed.rename(self.installed_backup)
            return True
        except OSError as e:
            logger.warning("Can't rename {} to {}"
                .format(self.installed, self.installed_backup))
            return False

    def _compute_actual(self):
        if str(self.source_relative).startswith('_'):
            self.source_relative = str(self.source_relative).replace('_', '.', 1)
        return Path.home() / self.source_relative

    def _compute_status(self):
        if not self.installed.exists():
            return Status.dont_exist

        if not self.installed.is_symlink():
            return Status.not_symlink

        target = os.readlink(str(self.installed))
        if str(target) != str(self.source):
            return Status.wrong_symlink

        if self.installed_backup.exists():
            return Status.to_merge

        return Status.ok
