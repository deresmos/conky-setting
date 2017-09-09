# imports {{{1
import os
from abc import abstractmethod
from os.path import expanduser
from subprocess import Popen, check_call, check_output


class ConkyConfWriter:
    H1_GOTO = 'goto 0'
    H2_GOTO = 'goto 20'
    H3_GOTO = 'goto 30'

    COLOR = 'color'
    COLOR2 = 'color2'

    BASE_FONT_SIZE = 9
    H1_FONT_SIZE = 'font :size={}'.format(int(BASE_FONT_SIZE * 1.6))
    H2_FONT_SIZE = 'font :size={}'.format(int(BASE_FONT_SIZE * 1.2))
    SMALL_FONT_SIZE = 'font :size={}'.format(int(BASE_FONT_SIZE * 0.9))

    @abstractmethod  # get_conf {{{2
    def get_conf(self):
        pass

    def _get_conf(self, main_text):
        with open(os.path.join(self.__config_path, 'base_setting.conf'),
                  'r') as f:
            conf_str = f.read()

        conf_str += self.get_config()
        conf_str += main_text + '\n]]\n'

        return conf_str

    @abstractmethod  # get_config {{{2
    def get_config(self):
        pass

    def _get_config(self, text):
        return text + '}\n\n' + 'conky.text = [[\n\n'

    def __init__(self, conf_filename):  # {{{2
        self.h1_goto = self.conky_esc(ConkyConfWriter.H1_GOTO)
        self.h2_goto = self.conky_esc(ConkyConfWriter.H2_GOTO)
        self.h3_goto = self.conky_esc(ConkyConfWriter.H3_GOTO)

        self.color = self.conky_esc(ConkyConfWriter.COLOR)
        self.color2 = self.conky_esc(ConkyConfWriter.COLOR2)

        self.h1_font_size = self.conky_esc(ConkyConfWriter.H1_FONT_SIZE)
        self.h2_font_size = self.conky_esc(ConkyConfWriter.H2_FONT_SIZE)
        self.small_font_size = self.conky_esc(ConkyConfWriter.SMALL_FONT_SIZE)

        path = os.path.dirname(os.path.realpath(__file__))
        self.__config_path = os.path.abspath(os.path.join(path, '../configs'))
        self.__tmp_path = os.path.abspath(os.path.join(path, '../tmp'))
        self._path = path

        self._conf_filename = conf_filename
        self.__save_path = os.path.join(self.__tmp_path, conf_filename)

    def conky_esc(self, text):  # {{{2
        return '${{{0}}}'.format(text)

    def save_conf(self):  # {{{2
        with open(self.__save_path, 'w') as f:
            f.write(self.get_conf())

    def h1(self, text):  # {{{2
        str = self.h1_goto + self.color + self.h1_font_size
        str += '{}  '.format(text)
        str += self.color2 + self.conky_esc('hr 4')
        str += self.color + self.conky_esc('font') + '\n'

        return str

    def h2(self, text):  # {{{2
        str = self.h2_goto + self.color + self.h2_font_size
        str += '{}  '.format(text)
        str += self.color2 + self.conky_esc('hr 2')
        str += self.color + self.conky_esc('font') + '\n'

        return str

