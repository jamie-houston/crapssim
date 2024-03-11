from colorama import Fore, Back, Style

class LogMixin(object):
    def __init__(self, verbose = False):
        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print(msg)

    def log_red(self, msg):
        self.log(Fore.RED + msg + Style.RESET_ALL)

    def log_green(self, msg):
        self.log(Fore.GREEN + msg + Style.RESET_ALL)