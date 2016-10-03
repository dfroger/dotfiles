#!/usr/bin/env python
from pathlib import Path
from logging import getLogger

import yaml

from .error import DotFilesException

logger = getLogger('dotfiles.config')

def get_dotfiles_dir(args):
    if args.dotfiles_dir != None:
        return Path(args.dotfiles_dir)

    fp = Path.home() / '.config' / 'dotfiles' / 'config.yaml'

    if fp.is_file():
        logger.debug('Read config file: {}'.format(fp))
        with fp.open() as f:
            data = yaml.load(f)
        return Path(data['dotfiles_dir'])
    else:
        logger.debug('No config file: {}'.format(fp))

    raise DotFilesException("Can't find dotfiles_dir")

