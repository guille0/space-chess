from distutils.core import setup
from Cython.Build import cythonize

import numpy

# BUILD WITH
# python3 ray/setup.py build_ext --inplace

setup(ext_modules=cythonize("ray/Ray.pyx"),
       include_dirs=[numpy.get_include()])
