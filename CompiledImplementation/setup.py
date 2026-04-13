from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Adds the Background Subtractor fike to be compiled
extensions = [
    Extension("BackgroundSubtractor", ["CompiledImplementation/BackgroundSubtractor.pyx"],
              include_dirs=[np.get_include()])
]

# Compiles using level 3
setup(
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)