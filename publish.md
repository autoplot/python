Read the Makefile to see how this is published to pypi.

To make a release:
1. after making and verifying edits for a release, update the version number in several places.
2. make sure setup.py has the same version number.
3. make test PYTHON=python  -- this is not working for me (can't find the python version)
4. make version-tag
5. make package
6. make release
   1. enter pypi password.

# Notes
## 2023-07-19
I was not able to get the commands at the top of the makefile to work with Python 3.10.  We should have instructions here, and link to this page in the readme.

I think I successfully did the pypi release (https://pypi.org/project/autoplot/), but it's not updating my machine when I do a 
"pip install autoplot".  I keep getting the old version.
