if __name__ == '__main__':  # {{{1
    from scripts import StartConky
    import sys
    import argparse
    from scripts import SystemConkyConf
    from scripts import InfoConkyConf

    parser = argparse.ArgumentParser(
        prog='conky setting script',
        description='Automatic conky setting creation')
    parser.add_argument(
        '--create',
        action='store_const',
        const=True,
        default=False,
        help='Create settings')
    parser.add_argument(
        '--run',
        action='store_const',
        const=True,
        default=False,
        help='Run conky')
    args = parser.parse_args()

    if args.create:
        info_conky = InfoConkyConf()
        info_conky.saveConf()
        system_conky = SystemConkyConf()
        system_conky.saveConf()
    elif args.run:
        conf_names = ['info.conf', 'system.conf']
        StartConky(conf_names).execute()
    else:
        parser.print_help()
