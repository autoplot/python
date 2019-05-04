# Make a release
#  git commit 
#  make test PYTHON=python2.7
#  make test PYTHON=python3.6
#  make version-tag VERSION=VERSION_IN_SETUP.PY
#  make release VERSION=VERSION_IN_SETUP.PY

#PYTHONV=2.7
PYTHONV=3.6

PYTHON=python$(PYTHONV)

URL=https://upload.pypi.org/

VERSION=0.0.2
SHELL:= /bin/bash

version-tag:
	git commit -a -m "Last $(VERSION) commit"
	git push
	git tag -a v$(VERSION) -m "Version "$(VERSION)
	git push --tags

package:
	make dist/hapiclient-$(VERSION).tar.gz

dist/autoplot-$(VERSION).tar.gz:
	python setup.py sdist

release: dist/autoplot-$(VERSION).tar.gz
	pip install twine
	twine upload \
		-r pypi dist/autoplot-$(VERSION).tar.gz \
		&& \
	echo Uploaded to $(subst upload.,,$(URL))/project/autoplot/

test:
	- conda create -n $(PYTHON) python=$(PYTHONV)
	source activate $(PYTHON); $(PYTHON) setup.py develop
	source activate $(PYTHON); $(PYTHON) -m pytest autoplot/test/test_autoplot.py

clean:
	- python setup.py --uninstall
	- find . -name __pycache__ | xargs rm -rf {}
	- find . -name *.pyc | xargs rm -rf {}
	- find . -name *.DS_Store | xargs rm -rf {}
	- find . -type d -name __pycache__ | xargs rm -rf {}
	- find . -type d -name ".egg-info" | xargs rm -rf {}
	- find . -name *.pyc | xargs rm -rf {}
	- rm -f *~
	- rm -f \#*\#
	- rm -rf env
	- rm -rf dist
	- rm -f MANIFEST
	- rm -rf .pytest_cache/
