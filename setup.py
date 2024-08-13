import sys
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from fluidframe_test.utilities.node_utils import check_node_installed, install_node

sys.dont_write_bytecode = True

class CustomBuild(build_py):
    def run(self):
        if not check_node_installed():
            install_node()
        # run_command(f"python setup.py build_ext --inplace", cwd=library_root)
        build_py.run(self)
        print("Build complete inside CustomBuild")
        

setup(
    name='fluidframe',
    version='0.1',
    author='Aswanth C Manoj',
    author_email='aswanthmanoj51@gmail.com',
    description="FluidFrame is a powerful, pythonic web application framework that embraces the simplicity and capability of hypermedia concepts. It combines Python's elegance with HTMX's innovative approach to create dynamic, interactive web applications without the need for complex JavaScript.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fluidframe=fluidframe.cli:main',
        ],
    },
    cmdclass={
        'build_py': CustomBuild,
    },
    package_data={
        'fluidframe_test': [
            'core/tags/*.pyi',
        ],
    },
    python_requires='>=3.10',
)