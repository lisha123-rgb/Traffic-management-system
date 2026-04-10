from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy
import os

# -------------------------------
# Hardcoded version (FIX)
# -------------------------------
VERSION = "1.0.0"

# -------------------------------
# Extensions
# -------------------------------
include_dirs = [numpy.get_include()]

ext_modules = [
    Extension(
        "darkflow.cython_utils.nms",
        sources=["darkflow/cython_utils/nms.pyx"],
        include_dirs=include_dirs,
        libraries=["m"] if os.name != "nt" else []
    ),
    Extension(
        "darkflow.cython_utils.cy_yolo2_findboxes",
        sources=["darkflow/cython_utils/cy_yolo2_findboxes.pyx"],
        include_dirs=include_dirs,
        libraries=["m"] if os.name != "nt" else []
    ),
    Extension(
        "darkflow.cython_utils.cy_yolo_findboxes",
        sources=["darkflow/cython_utils/cy_yolo_findboxes.pyx"],
        include_dirs=include_dirs,
        libraries=["m"] if os.name != "nt" else []
    )
]

# -------------------------------
# Setup
# -------------------------------
setup(
    name="darkflow",
    version=VERSION,
    description="Darkflow",
    license="GPLv3",
    url="https://github.com/thtrieu/darkflow",
    packages=find_packages(),
    scripts=["flow"],
    ext_modules=cythonize(ext_modules, language_level=3),
    zip_safe=False,
)