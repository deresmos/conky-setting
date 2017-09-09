# imports {{{1
import os

from .common import ConkyConfWriter
from subprocess import check_output
import re

# }}}1

class SystemConkyConf(ConkyConfWriter):
    def __init__(self):  # {{{2
        super().__init__('system.conf')

    def createGotos(self, array):  # {{{2
        gotos = []
        for num in array:
            gotos.append(self.conky_esc('goto {}'.format(num)))

        return gotos

    def getRam(self):  # {{{2
        str = self.h2('RAM  ${font}${memperc}%')
        str += self.h3_goto + self.color2 + 'Total'

        goto = self.createGotos([95, 165, 235, 305])

        str += goto[0] + 'Free' + goto[1] + 'Buffers'
        str += goto[2] + 'Cached' + goto[3] + 'Used'
        str += '\n'

        str += self.h3_goto + self.color + self.conky_esc('memmax')
        str += goto[0] + self.conky_esc('memfree') + \
            goto[1] + self.conky_esc('buffers')
        str += goto[2] + self.conky_esc('cached') + \
            goto[3] + self.conky_esc('mem')
        str += '\n'

        return str

    def getCpu(self):  # {{{2
        str = self.h2('CPU   ${font}${cpu}%')
        str += self.h3_goto
        str += self.conky_esc('execpi 3 python {}'.format(
            os.path.join(self._path, 'print_cpu.py')))

        str += '\n'
        return str

    def getTopProcess(self):  # {{{2
        goto = self.createGotos([75, 179, 234, 297])

        str = ''

        str += goto[0] + self.color + 'Name'
        str += goto[1] + 'PID'
        str += goto[2] + 'CPU%'
        str += goto[3] + 'MEM\n'

        str += self.h2('Top CPU')
        str += self.getTopCpu()

        str += self.h2('Top MEM')
        str += self.getTopMemory()

        return str

    def getTopCpu(self):  # {{{2
        goto = self.createGotos([30, 170, 230, 285])

        str = ''
        for x in range(1, 7):
            str += goto[0] + self.color2 + \
                self.conky_esc('top name {}'.format(x)) + self.color
            str += goto[1] + self.conky_esc('top pid {}'.format(x))
            str += goto[2] + self.conky_esc('top cpu {}'.format(x))
            str += goto[3] + self.conky_esc('top mem_res {}'.format(x)) + '\n'

        return str

    def getTopMemory(self):  # {{{2
        goto = self.createGotos([30, 170, 230, 285])

        str = ''
        for x in range(1, 7):
            str += goto[0] + self.color2 + \
                self.conky_esc('top_mem name {}'.format(x)) + self.color
            str += goto[1] + self.conky_esc('top_mem pid {}'.format(x))
            str += goto[2] + self.conky_esc('top_mem cpu {}'.format(x))
            str += goto[3] + \
                self.conky_esc('top_mem mem_res {}'.format(x)) + '\n'

        return str

    def getDev(self):  # {{{2
        res = check_output(['df']).decode('utf-8')
        match = re.findall(r'^(.+?)[ \t].+/$', res, re.MULTILINE)
        return match[0]

    def diskio(self):  # {{{2
        goto = self.createGotos([75, 130, 190])

        str = self.h2('Disk I/O')
        str += self.h3_goto + self.color2 + 'dev'
        str += goto[0] + 'write' + goto[1] + 'read'
        str += '\n'

        dev = self.getDev()
        str += self.h3_goto + self.color + dev
        str += goto[0] + self.conky_esc('diskio_write {}'.format(dev))
        str += goto[1] + self.conky_esc('diskio_read {}'.format(dev))
        str += '\n'

        str += self.conky_esc('voffset -25') + goto[2]
        str += self.conky_esc(
            'diskiograph {} 20, 160 303030 46afa7'.format(dev))
        str += '${voffset}\n'

        return str


    def network(self):  # {{{2
        goto = self.createGotos([200])

        wl = self.getEnv()
        str = self.conky_esc('voffset 5') + self.h2('Network')
        str += self.h3_goto + self.color2 + 'Down speed:'
        str += self.color + self.conky_esc('downspeed {}'.format(wl))
        str += goto[0] + self.color2 + 'Up speed:'
        str += self.color + self.conky_esc('upspeed {}'.format(wl))
        str += '\n'

        str += self.h3_goto + \
            self.conky_esc('downspeedgraph {} 20, 150 303030 00ff00'.format(wl))
        str += goto[0] + \
            self.conky_esc('upspeedgraph {} 20, 150 303030 ff0000'.format(wl))
        str += '\n'

        str += self.h3_goto + self.color2 + 'Toal down:'
        str += self.color + self.conky_esc('totaldown {}'.format(wl))

        str += goto[0] + self.color2 + 'Toal up:'
        str += self.color + self.conky_esc('totalup {}'.format(wl))
        str += '\n'

        return str

    def getEnv(self):  # {{{2
        try:
            res = check_output(['ifconfig']).decode('utf-8')
            match = re.findall(r'^(.*?):.*?[\r\n].*?broadcast', res, re.MULTILINE)
            return match[0]
        except:
            print('getEnv error')
            return None

    def get_config(self):  # {{{2
        str = '\talignment = \'top_left\',\n'
        str += "\tfont = ':size={}',\n".format(9)
        str += '\tupdate_interval = 3\n'

        return self._get_config(str)

    def get_conf(self):  # {{{2
        str = self.h1('RAM & CPU')
        str += self.getRam()
        str += self.getCpu()

        str += self.conky_esc('voffset -20')
        str += self.h1('Top Process')
        str += self.getTopProcess()
        str += '\n'

        str += self.h1('Disk I/O & Network')
        str += self.diskio()
        str += self.network()

        return self._get_conf(str)


if __name__ == '__main__':  # {{{1
    text = SystemConkyConf()
    print(text.get_conf())
