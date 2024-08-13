import os
import subprocess

def init(args):
    project_name = args.project_name
    fluidframe_dir = os.path.join(os.getcwd(), 'fluidframe')

    print(f"Initializing FluidFrame project: {project_name}")

    # Create fluidframe directory if it doesn't exist
    if not os.path.exists(fluidframe_dir):
        os.makedirs(fluidframe_dir)

    # Change to fluidframe directory
    os.chdir(fluidframe_dir)

    # Run npm init
    try:
        subprocess.run(['npm', 'init', '-y'], check=True)
        print(f"Successfully initialized npm project in {fluidframe_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing npm project: {e}")
        return

    # Update package.json with project name
    try:
        with open('package.json', 'r') as f:
            package_json = f.read()
        package_json = package_json.replace('"name": "fluidframe"', f'"name": "{project_name}"')
        with open('package.json', 'w') as f:
            f.write(package_json)
        print(f"Updated package.json with project name: {project_name}")
    except IOError as e:
        print(f"Error updating package.json: {e}")

    print(f"FluidFrame project '{project_name}' initialized successfully.")