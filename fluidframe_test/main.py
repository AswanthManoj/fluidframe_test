import argparse
from .commands import init, install

def main():
    parser = argparse.ArgumentParser(description='FluidFrame CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize FluidFrame')
    init_parser.add_argument('project_name', help='Name of the project to initialize')
    init_parser.set_defaults(func=init.init)

    # Install command
    install_parser = subparsers.add_parser('install', help='Install a Node.js package')
    install_parser.add_argument('package_name', help='Name of the package to install')
    install_parser.set_defaults(func=install.install)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()