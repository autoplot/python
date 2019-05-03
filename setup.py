from setuptools import setup, find_packages
import sys
import platform

if  platform.system() == 'Darwin':
    import os
    os.system("export MACOSX_DEPLOYMENT_TARGET=10.10")

install_requires = ["jpype1"]

if sys.argv[1] == 'develop':
    install_requires.append("pytest")

# version is modified by misc/setversion.py. See Makefile.
setup(
    name='autoplot',
    version='0.0.1',
    author='Jeremy Faden',
    author_email='faden@cottagesystems.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/autoplot/',
    license='LICENSE.txt',
    description='Interface to Autoplot library',
    long_description=open('README.rst').read(),
    install_requires=install_requires
)
