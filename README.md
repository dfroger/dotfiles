## Development

Require Python 3.5 and pyyaml:

    conda create -n dot python=3.5
    source activate dot

Install in development mode:

    pip install -e .

## Configuration

File `~/.config/dotfiles/config.yaml`

    dotfiles_path:
        - /path/to/your/versionned/dotfiles_base
        - /path/to/your/versionned/dotfiles_for_this_machine

Versionned config files can start with a `_` instead of `.`:

    /path/to/your/versionned/dotfiles/_bashrc
    /path/to/your/versionned/dotfiles/_config/something

## Usage

    usage: dot [-h] [--source_dir SOURCE_DIR] [--verbose] [--no-action]
                    {status,install}

    positional arguments:
      {status,install}

    optional arguments:
      -h, --help            show this help message and exit
      --source_dir SOURCE_DIR, -s SOURCE_DIR
                            Path to source directory
      --verbose, -v         Verbose mode
      --no-action, -n       Do not actually do anything, just log action
