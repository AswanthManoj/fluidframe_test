import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, cwd=cwd)
    process.wait()
    
def build_cython(library_root):
    run_command(f"python {library_root / 'setup.py'} build_ext --inplace", cwd=library_root)

