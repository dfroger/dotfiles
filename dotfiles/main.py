#!/usr/bin/env python
import logging

from .cmdline import parse_command_line
from .config import get_source_dir
from .context import Context
from .status import status
from .install import install
from .error import DotFilesException 
from .logger import configure_logger

def all():
    args = parse_command_line()
    configure_logger(args.verbose)
    source_dir = get_source_dir(args)
    context = Context(source_dir, no_action=args.no_action)
    dotfiles = context.find_dotfiles()

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
