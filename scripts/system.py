# imports {{{1
import os

from common import *


# functions {{{1
def create_gotos(array):  # {{{2
    gotos = []
    for num in array:
        gotos.append(esc('goto {}'.format(num)))

    return gotos


def ram():  # {{{2
    str = h2('RAM  ${font}${memperc}%')
    str += h3_goto + color2 + 'Total'

    goto = create_gotos([95, 165, 235, 305])

    str += goto[0] + 'Free' + goto[1] + 'Buffers'
    str += goto[2] + 'Cached' + goto[3] + 'Used'
    str += '\n'

    str += h3_goto + color + esc('memmax')
    str += goto[0] + esc('memfree') + goto[1] + esc('buffers')
    str += goto[2] + esc('cached') + goto[3] + esc('mem')
    str += '\n'

    return str


def cpu():  # {{{2
    str = h2('CPU   ${font}${cpu}%')
    str += h3_goto
    str += esc('execpi 3 python {}'.format(
        os.path.join(script_dir, 'print_cpu.py')))

    str += '\n'
    return str


def top_process():  # {{{2
    goto = create_gotos([75, 179, 234, 297])

    str = ''

    str += goto[0] + color + 'Name'
    str += goto[1] + 'PID'
    str += goto[2] + 'CPU%'
    str += goto[3] + 'MEM\n'

    str += h2('Top CPU')
    str += top_cpu()

    str += h2('Top MEM')
    str += top_mem()

    return str


def top_cpu():  # {{{2
    goto = create_gotos([30, 170, 230, 285])

    str = ''
    for x in range(1, 7):
        str += goto[0] + color2 + esc('top name {}'.format(x)) + color
        str += goto[1] + esc('top pid {}'.format(x))
        str += goto[2] + esc('top cpu {}'.format(x))
        str += goto[3] + esc('top mem_res {}'.format(x)) + '\n'

    return str


def top_mem():  # {{{2
    goto = create_gotos([30, 170, 230, 285])

    str = ''
    for x in range(1, 7):
        str += goto[0] + color2 + esc('top_mem name {}'.format(x)) + color
        str += goto[1] + esc('top_mem pid {}'.format(x))
        str += goto[2] + esc('top_mem cpu {}'.format(x))
        str += goto[3] + esc('top_mem mem_res {}'.format(x)) + '\n'

    return str


def getDev():  # {{{2
    command = 'df | grep -E "/$" | grep -o "^[^ ]*"'
    res = shell(command, var='co').decode()
    dev = res.split('/')[2].replace('\n', '')
    return dev


def diskio():  # {{{2

    goto = create_gotos([75, 130, 190])

    str = h2('Disk I/O')
    str += h3_goto + color2 + 'dev'
    str += goto[0] + 'write' + goto[1] + 'read'
    str += '\n'

    dev = getDev()
    str += h3_goto + color + dev
    str += goto[0] + esc('diskio_write {}'.format(dev))
    str += goto[1] + esc('diskio_read {}'.format(dev))
    str += '\n'

    str += esc('voffset -25') + goto[2]
    str += esc('diskiograph {} 20, 160 303030 46afa7'.format(dev))
    str += '${voffset}\n'

    return str


def network():  # {{{2
    goto = create_gotos([200])

    wl = getEnv()
    str = esc('voffset 5') + h2('Network')
    str += h3_goto + color2 + 'Down speed:'
    str += color + esc('downspeed {}'.format(wl))
    str += goto[0] + color2 + 'Up speed:'
    str += color + esc('upspeed {}'.format(wl))
    str += '\n'

    str += h3_goto + esc('downspeedgraph {} 20, 150 303030 00ff00'.format(wl))
    str += goto[0] + esc('upspeedgraph {} 20, 150 303030 ff0000'.format(wl))
    str += '\n'

    str += h3_goto + color2 + 'Toal down:'
    str += color + esc('totaldown {}'.format(wl))

    str += goto[0] + color2 + 'Toal up:'
    str += color + esc('totalup {}'.format(wl))
    str += '\n'

    return str


def getEnv():  # {{{2
    str = ''
    try:
        str = shell(
            "ifconfig | grep -B1 broadcast | grep -o '^[^:]\+\?'", var='co')
    except:
        print('getEnv error')
        return None
    return str.decode().split('\n')[0]


def config():  # {{{2
    str = '\talignment = \'top_left\',\n'
    str += "\tfont = ':size={}',\n".format(font_size)
    str += '\tupdate_interval = 3\n'

    return str + '}\n\n'


def generate_sys_conf():  # {{{2
    str = config()

    str += 'conky.text = [[\n\n'

    str += h1('RAM & CPU')
    str += ram()
    str += cpu()

    str += esc('voffset -20')
    str += h1('Top Process')
    str += top_process()
    str += '\n'

    str += h1('Disk I/O & Network')
    str += diskio()
    str += network()

    str += '\n]]\n'

    return str


# }}}1 END functions

if __name__ == '__main__':  # {{{1

    with open(os.path.join(config_dir, 'system.conf'), 'w') as f:
        f.write(generate_sys_conf())
