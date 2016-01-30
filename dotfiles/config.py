#!/usr/bin/env python
from pathlib import Path
from logging import getLogger

import yaml

from .error import DotFilesException

logger = getLogger('dotfiles.config')

def get_source_dir(args):
    if args.source_dir != None:
        return Path(args.source_dir)

    fp = Path.home() / '.config' / 'dotfiles' / 'config.yaml'

    if fp.is_file():
        logger.debug('Read config file: {}'.format(fp))
        with fp.open() as f:
            data = yaml.load(f)
        return Path(data['source_dir'])
    else:
        logger.debug('No config file: {}'.format(fp))

    raise DotFilesException("Can't find source_dir")

