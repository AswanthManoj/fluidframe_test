import sys, os
import subprocess
from Cython.Build import cythonize
from setuptools.command.build_py import build_py
from setuptools import setup, find_packages, Extension
from fluidframe_test.utilities.node_utils import check_node_installed, install_node

sys.dont_write_bytecode = True

class CustomBuild(build_py):
    def run(self):
        if not check_node_installed():
            install_node()
        self.create_fluidframe_node_module()
        print("Build complete inside with node installation check and package.json installation for installing FluidFrame dependencies")
        build_py.run(self)
    
    def create_fluidframe_node_module(self):
        # Create node_modules for FluidFrame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fluidframe_dir = os.path.join(current_dir, 'fluidframe_test')
        os.chdir(fluidframe_dir)
        try:
            subprocess.run(['npm', 'install'], check=True)
            print("Successfully installed FluidFrame dependencies")
        except subprocess.CalledProcessError as e:
            print(f"Error installing FluidFrame dependencies: {e}")
        os.chdir(current_dir)
        
 
extensions = [
    Extension(
        "fluidframe_test.core.tags.tags", 
        ["fluidframe_test/core/tags/tags.pyx"],
        extra_compile_args=["-O3"], 
        extra_link_args=["-O3"],
        py_limited_api=True
    )
]
       

setup(
    name='fluidframe',
    version='0.1',
    author='Aswanth C Manoj',
    author_email='aswanthmanoj51@gmail.com',
    description="FluidFrame is a powerful, pythonic web application framework that embraces the simplicity and capability of hypermedia concepts. It combines Python's elegance with HTMX's innovative approach to create dynamic, interactive web applications without the need for complex JavaScript.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["fluidframe_test", "fluidframe_test.*"]),
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
            'node_modules/**/*',
        ],
    },
    python_requires='>=3.10',
    ext_modules=cythonize(extensions, language_level="3"),
)