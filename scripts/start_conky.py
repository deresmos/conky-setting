# imports {{{1
import os

try:
    from .common import *
except:
    from common import *


class StartConky:  # {{{1
    EXECUTE = 1
    ONLY_EXECUTE = 2

    def __init__(self, conf_names, script_names=None):  # {{{2
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(os.path.join(path, '..'))
        self.conf_dir = os.path.join(path, 'configs')
        self.script_dir = os.path.join(path, 'scripts')
        self.save_dir = os.path.join(path, 'tmp')

        base_path = os.path.join(self.conf_dir, 'base_setting.conf')
        self.base_settings = readfile(base_path)
        self.script_names = script_names
        self.save_paths = [
            os.path.join(self.save_dir, name) for name in conf_names
        ]
        self.configs = [
            os.path.join(self.conf_dir, name + '.conf') for name in conf_names
        ]

    def run(self, isRun):  # {{{2
        if isRun == StartConky.ONLY_EXECUTE:
            self.execute()
            return

        self.generate_configs()
        if isRun == StartConky.EXECUTE:
            self.execute()

    def generate_configs(self):  # {{{2
        for path in self.script_names:
            command = 'python {}.py'.format(
                os.path.join(self.script_dir, path))
            shell(command, var='co')

        for i, config in enumerate(self.configs):
            str = self.base_settings + readfile(config)
            with open(self.save_paths[i], 'w') as f:
                f.write(str)

    def execute(self):  # {{{2
        for config in self.save_paths:
            str = 'conky -c {}'.format(config)
            print(str)
            shell(str)


# }}}1
