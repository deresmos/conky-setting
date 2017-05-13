# imports {{{1
import os

import print_cal
from common import *


def config():  # {{{1
    str = ''

    return str + '}\n\n'


def generate_info_conf():  # {{{1
    str = config()

    str += 'conky.text = [[\n\n'

    str += '''
${voffset -8}$alignr$color${font Bitstream Vera Sans:size=30}${time %Y}$font
$color${voffset -30}$color${font Bitstream Vera Sans:size=20}${time %m}$font\
${voffset -3} $color${font Bitstream Vera Sans:size=22}${time %d}$font$color2$hr
$alignc$color${font :size=36}${time %H}:${time %M}
'''
    str += h2('INFORMATION')
    str += '''
${goto 40}${color2}HDD FREE:$alignr$color${fs_free} / ${fs_size}
${goto 40}${color2}HDD:$color$fs_used_perc% ${fs_bar 6}

${voffset 10}${goto 40}${color}Swap${font Bitstream Vera Sans:bold:size=8}$alignr${swap}/ ${swapfree}
${voffset 15}$font$alignr${execi 10000 awk -F= '/TION/ {print $2}' /etc/lsb-release |sed 's/"//g'} \
${execi 10000 awk -F= '/EASE=/ {printf $2" "} /NAME/ {print $2}' /etc/lsb-release}
${voffset 10}${color2}${alignr}${execi 1200 whoami}@${nodename}
${alignr}${color2}${font Bitstream Vera Sans:size=8}uptime: ${color}${uptime_short}
${voffset 5}${color2}${font Bitstream Vera Sans:size=8}${alignr}kernel: ${color}${kernel}
'''

    str += h2('Calendar')
    str += print_cal.createCal()

    str += '\n]]\n'
    return str


if __name__ == '__main__':  # {{{1
    import common
    with open(os.path.join(common.config_dir, 'info.conf'), 'w') as f:
        f.write(generate_info_conf())
