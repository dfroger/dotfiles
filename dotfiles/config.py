#!/usr/bin/env python
from pathlib import Path
from logging import getLogger

import yaml

from .error import DotFilesException

logger = getLogger('dotfiles.config')

def get_dotfiles_path(args):
    if args.dotfiles_path != None:
        return args.dotfiles_path

    config = Path.home() / '.config' / 'dotfiles' / 'config.yaml'

    if config.is_file():
        logger.debug('Read config file: {}'.format(config))
        with config.open() as f:
            data = yaml.load(f)
        return data['dotfiles_path']
    else:
        logger.debug('No config file: {}'.format(config))

    raise DotFilesException("Can't find dotfiles_dir")


def get_dotfiles_dirs(args):
    dotfiles_path = get_dotfiles_path(args)
    return [Path(p) for p in dotfiles_path.split(':')]
