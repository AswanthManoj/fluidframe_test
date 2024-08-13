import os
import subprocess
import importlib.util

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

def get_package_path():
    """Get the absolute path to the installed FluidFrame package."""
    spec = importlib.util.find_spec("fluidframe_test")
    if spec is None:
        raise ImportError("FluidFrame package not found")
    return os.path.dirname(spec.origin)

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
    package_path = get_package_path()
    
    library_files = [
        os.path.join(package_path, "core", "components", "**", "*.py"),
        os.path.join(package_path, "templates", "**", "*.html"),
    ]

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