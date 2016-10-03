from logging import getLogger
import shutil

from .dotfile import Status

logger = getLogger('dotfiles.install')

def install(dotfile):
    logger.debug('Installing {}'.format(dotfile.source_relative))

    if dotfile.status == Status.ok:
        logger.debug('{} is already installed'.
            format(dotfile.actual))
        return

    elif dotfile.status == Status.missing:
        shutil.copy(str(dotfile.dotfile), str(dotfile.actual))
