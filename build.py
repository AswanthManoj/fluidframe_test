from Cython.Build import cythonize
from setuptools import Extension

def build(setup_kwargs):
    extensions = [
        Extension(
            "fluidframe_test.core.tags.tags",
            ["fluidframe_test/core/tags/tags.pyx"],
            extra_compile_args=["-O3"],
            extra_link_args=["-O3"],
            py_limited_api=True
        )
    ]
    setup_kwargs.update({
        'ext_modules': cythonize(extensions, language_level="3"),
    })