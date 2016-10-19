## Install

Require Python 3.5 and pyyaml.

    python setup.py install

## Configuration

File `~/.config/dotfiles/config.yaml`

    dotfiles_path: /path/to/your/versionned/dotfiles

Versionned config files can start with a `_` instead of `.`:

    /path/to/your/versionned/dotfiles/_bashrc
    /path/to/your/versionned/dotfiles/_config/something

## Usage

    usage: dotfiles [-h] [--source_dir SOURCE_DIR] [--verbose] [--no-action]
                    {status,install}

    positional arguments:
      {status,install}

    optional arguments:
      -h, --help            show this help message and exit
      --source_dir SOURCE_DIR, -s SOURCE_DIR
                            Path to source directory
      --verbose, -v         Verbose mode
      --no-action, -n       Do not actually do anything, just log action
