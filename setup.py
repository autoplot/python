try:
    from setuptools import setup, find_packages
except ImportError:
    print('setuptools not available. Try:\n\tpip install setuptools --user')

import sys
import platform

if platform.system() == 'Darwin':
    import os
    os.system("export MACOSX_DEPLOYMENT_TARGET=10.10")

install_requires = ["install-jdk","jpype1","numpy"]

if sys.argv[1] == 'develop':
    install_requires.append("pytest")

setup(
    name='autoplot',
    version='0.9.5',
    author='Jeremy Faden',
    author_email='faden@cottagesystems.com',
    packages=find_packages(), 
    url='https://github.com/autoplot/python/',
    license='LICENSE.txt',
    description='Interface to Autoplot Java library',
    long_description=open('README.rst', encoding='utf-8').read(),
    long_description_content_type='text/x-rst',
    install_requires=install_requires
)

