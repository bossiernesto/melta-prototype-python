import sys
import readline


class Console(object):
    def __init__(self, complete_key='tab', stdin=None, stdout=None):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.complete_key = complete_key
        self.cmd_queue = []
        self.command_history = ConsoleHistory()

    def backup_completer(self):
        try:
            self.old_completer = readline.get_completer()
            readline.set_completer(self.complete)
            readline.parse_and_bind("{0}: complete".format(self.complete_key))
        except ImportError:
            ConsoleError('couldn\'t put new completer')

    def restore_completer(self):
        readline.set_completer(self.old_completer)

    def primary_loop_cmd(self):

        self.before_command_loop()
        self.after_command_loop()

    def complete(self):
        pass

class ConsoleHistory(list):
    def __init__(self, *args):
        list.__init__(self, *args)


class ConsoleError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)