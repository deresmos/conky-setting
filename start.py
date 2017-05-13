if __name__ == '__main__':  # {{{1
    from scripts import StartConky
    import sys

    conf_names = ['info', 'system']
    script_names = ['info', 'system']
    if len(sys.argv) != 2:
        StartConky(conf_names, script_names).run(0)
    else:
        StartConky(conf_names, script_names).run(int(sys.argv[1]))

    exit(0)
