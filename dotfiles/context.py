#!/usr/bin/env python
from pathlib import Path

from .dotfile import DotFile

class Context:

    def __init__(self, source_dir, *, install_dir=Path.home(),
                 no_action=False):
        self.install_dir = Path(install_dir)
        self.source_dir = Path(source_dir)
        self.no_action = no_action

    def find_dotfiles(self):
        dotfiles = []
        for p in self.source_dir.glob('**/*'):
            if p.is_dir():
                continue
            source_relative = p.relative_to(self.source_dir)
            dotfiles.append( DotFile(self, source_relative) )
        return dotfiles
