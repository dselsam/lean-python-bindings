from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
import shutil
import subprocess

from setuptools import setup, find_packages, Distribution
import setuptools.command.build_ext as _build_ext

class build_ext(_build_ext.build_ext):

    def run(self):
        # We build the C++ extension in a different directory to avoid
        # having build artifacts in the package directory and make it
        # easy to clean the build. This means we need to move the files
        # here.
        subprocess.check_call(["./build.sh"])
        for path in glob.glob("build/lean.cpython*"):
            directory, filename = os.path.split(path)
            destination = os.path.join("lean", filename)
            print("Copying {} to {}".format(path, destination))
            shutil.copy(path, destination)

class BinaryDistribution(Distribution):

    def has_ext_modules(self):
        return True

setup(name="lean",
      version="0.0.1",
      packages=find_packages(),
      install_requires=["numpy", "scipy", "tensorflow"],
      cmdclass={"build_ext": build_ext},
      # The BinaryDistribution argument triggers build_ext
      distclass=BinaryDistribution,
      include_package_data=True,
      zip_safe=False,
      license="Apache 2.0")
