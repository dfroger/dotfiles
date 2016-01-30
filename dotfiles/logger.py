import logging

def configure_logger(verbose):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    formatter = logging.Formatter(
        fmt = '%(name)-16s: %(levelname)-8s: %(message)s',)

    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(level)

    logger = logging.getLogger('dotfiles')
    logger.addHandler(consolehandler)
    logger.setLevel(level)
