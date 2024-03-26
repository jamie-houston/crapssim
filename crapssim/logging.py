from colorama import Fore, Back, Style


def log(msg, verbose=True):
    if verbose:
        print(msg)


def log_red(msg, verbose=True):
    log(Fore.RED + msg + Style.RESET_ALL, verbose)


def log_green(msg, verbose=True):
    log(Fore.GREEN + msg + Style.RESET_ALL, verbose)


def log_yellow(msg, verbose=True):
    log(Fore.YELLOW + msg + Style.RESET_ALL, verbose)
