import os
import subprocess

def install(args):
    package_name = args.package_name
    fluidframe_dir = os.path.join(os.getcwd(), 'fluidframe')

    if not os.path.exists(fluidframe_dir):
        print("Error: FluidFrame directory not found. Please run 'fluidframe init <project_name>' first.")
        return

    os.chdir(fluidframe_dir)

    print(f"Installing Node.js package: {package_name}")

    try:
        subprocess.run(['npm', 'install', package_name], check=True)
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}")