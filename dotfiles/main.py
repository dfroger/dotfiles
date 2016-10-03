#!/usr/bin/env python
import logging

from .cmdline import parse_command_line
from .config import get_dotfiles_dir
from .status import status
from .install import install
from .error import DotFilesException
from .logger import configure_logger
from .dotfile import find_dotfiles

def all():
    args = parse_command_line()
    configure_logger(args.verbose)
    dotfiles_dir = get_dotfiles_dir(args)
    dotfiles = find_dotfiles(dotfiles_dir)

    if args.action == 'status':
        for dotfile in dotfiles:
            status(dotfile)

    elif args.action == 'install':
        for dotfile in dotfiles:
            install(dotfile)

def main():
    try:
        all()
    except DotFilesException as e:
        logger.critical(e)

if __name__ == '__main__':
        main()
