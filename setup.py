import sys
from pathlib import Path
from Cython.Build import cythonize
from setuptools.command.build_py import build_py
from setuptools import setup, find_packages, Extension
from fluidframe_test.utilities.cython_build import build_cython
from fluidframe_test.utilities.node_utils import check_node_installed, install_node

sys.dont_write_bytecode = True

class CustomBuild(build_py):
    def run(self):
        library_root = Path(__file__).parent
        build_cython(library_root)
        if not check_node_installed():
            install_node()
        print("Build complete inside CustomBuild")
        build_py.run(self)
        
 
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
        ],
    },
    python_requires='>=3.10',
    ext_modules=cythonize(extensions, language_level="3"),
)