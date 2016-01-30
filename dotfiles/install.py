from logging import getLogger

from .dotfile import Status

logger = getLogger('dotfiles.install')

def install(dotfile):
    logger.debug('Installing {}'.format(dotfile.source_relative))

    if dotfile.status == Status.ok:
        logger.debug('{} is already installed'.
            format(dotfile.installed))
        return

    elif dotfile.status == Status.dont_exist:
        dotfile.symlink()

    elif dotfile.status in (Status.not_symlink, Status.wrong_symlink):
        if not dotfile.backup():
            return
        dotfile.symlink()
