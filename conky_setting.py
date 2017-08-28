if __name__ == '__main__':  # {{{1
    from scripts import StartConky
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        prog='conky setting script',
        description='Automatic conky setting creation')
    parser.add_argument(
        '--setup',
        action='store_const',
        const=True,
        default=False,
        help='Start conky and create settings')
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

    conf_names = ['info', 'system']
    script_names = ['info', 'system']

    if args.setup:
        StartConky(conf_names, script_names).run(StartConky.SETUP)
    elif args.create:
        StartConky(conf_names, script_names).run(StartConky.CREATE)
    elif args.run:
        StartConky(conf_names, script_names).run(StartConky.RUN)
    else:
        parser.print_help()
