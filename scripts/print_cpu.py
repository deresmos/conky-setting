from subprocess import check_output

command = "cat /proc/cpuinfo | grep MHz | awk '{print $4}'"

cpu_freqs = [
    freq for freq in check_output(
        command, shell=True, var='co').decode().split('\n') if freq != ''
]

command = 'cat /proc/cpuinfo | grep "model name" | grep -o ":.*"'
res = check_output(command, shell=True, var='co').decode().split('\n')
cpu_info = res[0].split(': ')[1]
print('${alignr}${color2}' + cpu_info)

str = ''
cpu_str = '${{goto 30}}${{color2}}CPU Core {1}: ${{color}}{0} Mhz '
cpu_str += '${{goto 200}}${{color2}}Load: ${{color}}${{cpu cpu{1}}}%\n'
for i, freq in enumerate(cpu_freqs):
    core_index = i + 1
    str += cpu_str.format(freq, core_index)
    str += '${{goto 30}}${{cpugraph cpu{} 17,300 303030 467f77}}\n'.format(
        core_index)

print(str)
