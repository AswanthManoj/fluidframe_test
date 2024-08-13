import argparse
from .commands import init, install, watch

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
    
    # In the main() function, add:
    watch_parser = subparsers.add_parser('watch', help='Start Tailwind CSS watch process')
    watch_parser.set_defaults(func=watch.watch)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()




# Then create a new file fluidframe/commands/watch.py:
import os
import subprocess

def watch(args):
    fluidframe_dir = os.path.join(os.getcwd(), 'fluidframe')
    if not os.path.exists(fluidframe_dir):
        print("Error: FluidFrame directory not found. Please run 'fluidframe init <project_name>' first.")
        return

    os.chdir(fluidframe_dir)
    try:
        subprocess.run(['npx', 'tailwindcss', '-i', 'input.css', '-o', 'dist/output.css', '--watch'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Tailwind watch process: {e}")
    except KeyboardInterrupt:
        print("Tailwind watch process stopped.")