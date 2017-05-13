# imports {{{1
import os
from subprocess import Popen, check_call, check_output


def esc(str):  # {{{1
    return '${{{0}}}'.format(str)


# variables {{{1
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, '..')

h1_goto = 'goto 0'
h2_goto = 'goto 20'
h3_goto = 'goto 30'

color = 'color'
color2 = 'color2'

font_size = 9
h1_font = 'font :size={}'.format(int(font_size * 1.6))
h2_font = 'font :size={}'.format(int(font_size * 1.2))
small_font = 'font :size={}'.format(int(font_size * 0.9))

h1_goto = esc(h1_goto)
h2_goto = esc(h2_goto)
h3_goto = esc(h3_goto)

h1_font = esc(h1_font)
h2_font = esc(h2_font)
small_font = esc(small_font)

color = esc(color)
color2 = esc(color2)

script_dir = os.path.join(path, 'scripts')
config_dir = os.path.join(path, 'configs')


# functions {{{1
def h1(title):  # {{{1
    str = h1_goto + color
    str += h1_font
    str += '{}  '.format(title)
    str += color2 + esc('hr 4')
    str += color + esc('font') + '\n'

    return str


def h2(title):  # {{{1
    str = h2_goto + color + h2_font
    str += '{}  '.format(title)
    str += color2 + esc('hr 2')
    str += color + esc('font') + '\n'

    return str


def readfile(filepath):  # {{{1
    with open(filepath) as f:
        return f.read()


def shell(command, shell=True, var=None):  # {{{1
    if var == 'cc':
        return check_call(command, shell=shell)
    elif var == 'co':
        return check_output(command, shell=shell)
    else:
        return Popen(command, shell=shell)


def file_pwd():  # {{{1
    return os.path.dirname(os.path.realpath(__file__))
