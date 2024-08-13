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