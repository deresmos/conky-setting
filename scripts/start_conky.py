# imports {{{1
import os
from subprocess import check_output


class StartConky:  # {{{1
    def __init__(self, conf_names):  # {{{2
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(os.path.join(path, '..'))
        self.conf_dir = os.path.join(path, 'configs')
        self.script_dir = os.path.join(path, 'scripts')
        self.save_dir = os.path.join(path, 'tmp')

        self.save_paths = [
            os.path.join(self.save_dir, name) for name in conf_names
        ]
        self.configs = [
            os.path.join(self.conf_dir, name + '.conf') for name in conf_names
        ]

    def execute(self):  # {{{2
        for config in self.save_paths:
            str = 'conky -c {}'.format(config)
            check_output(['conky', '-c', config])
            print(str)


# }}}1
