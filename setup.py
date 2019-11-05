import os
import sys

from setuptools import setup, find_packages

SETUP_DIR = os.path.abspath(os.path.dirname(__file__))


def _find_toplevel(target):
    """return the toplevel of git repository or throw IOError"""
    git_config = os.path.join(target, '.git', 'config')
    if os.path.exists(git_config):
        return target
    target_parent = os.path.dirname(target)
    if target_parent == target:  # check to see if at root to mitigate infinite recursion
        raise IOError("Could not find .git/config")
    else:
        return _find_toplevel(target_parent)


TLDIR = _find_toplevel(SETUP_DIR)

package_name = 'stronz'
description = 'A python package for stro.nz'

with open(os.path.join(TLDIR, 'README.md')) as fhandle:
    readme = fhandle.read()
requirements = ['tldextract', 'tornado']
long_description = readme
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
      setup_requires=requirements,
      license=package.__license__
      )
