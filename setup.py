import os
import sys

from setuptools import setup, find_packages

package_name = 'personalwebsite'
description = 'A python2 library to encapsulate my personal website'
readme = open('README.md').read()
requirements = ['deveta']
long_description = open('README.md').read()
package = __import__(package_name)

package_version = package.__version__

setup(name=package_name,
      version=package_version,
      author=package.__author__,
      author_email=package.__author_email__,
      url=package.__url__,
      description=description,
      long_description=long_description,
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      license=package.__license__
)
