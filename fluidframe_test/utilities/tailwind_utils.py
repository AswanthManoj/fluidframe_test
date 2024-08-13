import os
import subprocess

def tailwind_build(args):
    """
    Builds the Tailwind CSS for a FluidFrame project.

    Parameters:
    args (object): An object containing the project arguments.

    Returns:
    None

    The function checks if the FluidFrame directory exists, changes to it, and runs the Tailwind build process.
    If the directory does not exist, it prints an error message and returns.
    If the build process fails, it catches the exception and prints an error message.
    """
    fluidframe_dir = os.path.join(os.getcwd(), 'fluidframe')
    if not os.path.exists(fluidframe_dir):
        print("Error: FluidFrame directory not found. Please run 'fluidframe init <project_name>' first.")
        return

    os.chdir(fluidframe_dir)
    try:
        subprocess.run(['npx', 'tailwindcss', '-i', 'input.css', '-o', 'dist/output.css'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error on Tailwind build process: {e}")
    except KeyboardInterrupt:
        print("Tailwind build process stopped.")

        
def generate_tailwind_config(fluidframe_dir):
    """
    Generates a Tailwind configuration file for a FluidFrame project.

    Parameters:
    fluidframe_dir (str): The directory path of the FluidFrame project.

    Returns:
    None

    The function generates a tailwind.config.js file in the specified FluidFrame project directory.
    It includes the library files and user project files in the content section of the configuration.
    """
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
{''.join([f"    '{f}',\n" for f in library_files])}
    // User project files
    '../src/**/*.{{html,py}}'
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