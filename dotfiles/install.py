from logging import getLogger
import shutil

from .dotfile import Status

logger = getLogger('dotfiles.install')

def install(dotfile, no_action):
    logger.debug('Installing {}'.format(dotfile.relative_path))

    action = not no_action

    if dotfile.status == Status.ok:
        logger.debug('{} is already installed'. format(dotfile.actual))
        return

    elif dotfile.status == Status.missing:
        directory = dotfile.actual.parent
        if not directory.is_dir():
            print('mkdir -p {}'.format(directory))
            if action:
                directory.mkdir(parents=True)

        print('cp {} {}'.format(str(dotfile.dotfile), str(dotfile.actual)))
        print()
        if action:
            shutil.copy(str(dotfile.dotfile), str(dotfile.actual))
