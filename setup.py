from setuptools import setup

setup(
    name = 'dotfiles',
    version = '0.1.0',
    description = 'Manage your versionned dot files.',
    url = 'https://github.com/dfroger/dotfiles',
    packages = ['dotfiles',],
    entry_points = {
        'console_scripts': [
            'dot = dotfiles.main:main',
        ],
    },
    license = 'GPL V3',
    author = 'David Froger',
    author_email = 'david.froger@mailoo.org',
    install_requires=[
        'pyyaml',
    ]
)
