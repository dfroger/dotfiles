## Configuration

File `~/.config/dotfiles/config.json`

    dotfiles_path:
    {
        "backup": [
            "/path/to/your/versionned/dotfiles_base",
            "/path/to/your/versionned/dotfiles_for_this_machine"
        ]
}

Versionned config files can start with a `_` instead of `.`:

    /path/to/your/versionned/dotfiles/_bashrc
    /path/to/your/versionned/dotfiles/_config/something
