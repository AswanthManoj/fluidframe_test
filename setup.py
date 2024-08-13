from setuptools import setup, find_packages

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
    python_requires='>=3.10'
)