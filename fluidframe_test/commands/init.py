'''import os
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
'''

import os
import json
import shutil
import subprocess

import os
import json
import shutil
import subprocess

def init(args):
    project_name = args.project_name
    current_dir = os.getcwd()
    fluidframe_dir = os.path.join(current_dir, 'fluidframe')
    utilities_dir = os.path.join(os.path.dirname(__file__), '..', 'utilities')

    print(f"Initializing FluidFrame project: {project_name}")

    # Create fluidframe directory if it doesn't exist
    if not os.path.exists(fluidframe_dir):
        os.makedirs(fluidframe_dir)

    # Copy package.json and package-lock.json from utilities
    shutil.copy(os.path.join(utilities_dir, 'package.json'), fluidframe_dir)
    shutil.copy(os.path.join(utilities_dir, 'package-lock.json'), fluidframe_dir)

    # Update package.json with project name
    package_json_path = os.path.join(fluidframe_dir, 'package.json')
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
    
    package_data['name'] = project_name
    
    with open(package_json_path, 'w') as f:
        json.dump(package_data, f, indent=2)

    # Generate tailwind.config.js
    generate_tailwind_config(fluidframe_dir)

    # Create input.css
    input_css_path = os.path.join(fluidframe_dir, 'input.css')
    with open(input_css_path, 'w') as f:
        f.write('@tailwind base;\n@tailwind components;\n@tailwind utilities;\n')

    # Change to fluidframe directory
    os.chdir(fluidframe_dir)

    # Install dependencies
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("Successfully installed dependencies")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return

    # Run initial Tailwind build
    try:
        subprocess.run(['npx', 'tailwindcss', '-i', 'input.css', '-o', 'dist/output.css'], check=True)
        print("Successfully built initial CSS")
    except subprocess.CalledProcessError as e:
        print(f"Error building initial CSS: {e}")

    print(f"FluidFrame project '{project_name}' initialized successfully.")
    print("To start Tailwind CSS watching for changes, run:")
    print(f"cd {fluidframe_dir} && npx tailwindcss -i input.css -o dist/output.css --watch")

    # Change back to original directory
    os.chdir(current_dir)

def generate_tailwind_config(fluidframe_dir):
    library_files = [
        "./fluidframe/core/components.py",
        "./fluidframe/components/**/*.py",
        "./fluidframe/templates/index.html"
    ]

    # Get the relative path from the user's project to the installed fluidframe package
    fluidframe_package_path = os.path.dirname(os.path.dirname(__file__))
    relative_path = os.path.relpath(fluidframe_package_path, fluidframe_dir)

    # Prepend the relative path to each library file
    library_files = [os.path.join(relative_path, file) for file in library_files]

    config_content = f"""
module.exports = {{
  content: [
    // Library files
    {json.dumps(library_files)},
    // User project files
    '../**/*.{{html,js,jsx,ts,tsx,py}}',
  ],
  theme: {{
    extend: {{}},
  }},
  plugins: [],
}}
"""

    config_path = os.path.join(fluidframe_dir, 'tailwind.config.js')
    with open(config_path, 'w') as f:
        f.write(config_content)

    print(f"Generated tailwind.config.js at {config_path}")