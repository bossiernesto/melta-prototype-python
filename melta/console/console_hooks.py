class ConsoleHook(object):
    def execute(self, console):
        raise NotImplementedError


class LoopHooks(object):
    def __init__(self, console):
        self.post_hooks = []
        self.pre_hooks = []
        self.console = console

    def execute(self, hook_name):
        for hook in getattr(self, hook_name):
            hook.execute(self.console)

    def execute_pre(self):
        return self.execute('pre_hooks')

    def execute_post(self):
        return self.execute('post_hooks')

    def add_pre_hook(self, hook):
        if isinstance(hook, ConsoleHook):
            self.pre_hooks.append(hook)

    def add_post_hook(self, hook):
        if isinstance(hook, ConsoleHook):
            self.post_hooks.append(hook)