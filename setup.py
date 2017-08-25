from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import subprocess

from setuptools import setup, find_packages, Distribution
import setuptools.command.build_ext as _build_ext

class build_ext(_build_ext.build_ext):
    def run(self):
        subprocess.check_call(["./build.sh"])

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(name="lean",
      version="0.0.1",
      packages=find_packages(),
      cmdclass={"build_ext": build_ext},
      # The BinaryDistribution argument triggers build_ext
      distclass=BinaryDistribution,
      include_package_data=True,
      zip_safe=False,
      license="Apache 2.0")
