import sys

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Adds the Background Subtractor fike to be compiled
if sys.platform == 'win32':
    # Windows (MSVC) flags
    compile_args = ['/O2', '/arch:AVX2', '/fp:fast']
else:
    # Linux (GCC/Clang) flags
    compile_args = ['-O3', '-march=native', '-ffast-math']

extensions = [
    Extension(
        "BackgroundSubtractor",
        ["CompiledImplementation/BackgroundSubtractor.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=compile_args,
    ),
    Extension(
        "ObjectTracker",
        ["CompiledImplementation/ObjectTracker.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=compile_args,
    ),
]

# Compiles using level 3
setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "boundscheck": False,  # Remove for speed
            "wraparound": False,  # Remove for speed
            "initializedcheck": False,
            "language_level": "3",
        },
    ),
)
