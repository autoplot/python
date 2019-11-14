# To make a release, edit `version` keyword in setup.py and
# modify make commands below accordingly. Then
#   git commit
#   make test PYTHON=python2.7
#   make test PYTHON=python3.6
#   make version-tag VERSION=0.0.2
#   echo "One must manually update the version in setup.py"
#   make package VERSION=0.0.2
#   make release VERSION=0.0.2

SHELL:= /bin/bash
VERSION=0.1.3  # should match setup.py
PYTHONV=3.6
PYTHON=python$(PYTHONV)
URL=https://upload.pypi.org/

version-tag: version-tag-commit version-tag-push

version-tag-commit:
	echo "VERSION=$(VERSION)"
	- git commit -a -m "Last $(VERSION) commit"
	echo "done commit"	
	git push
	echo "done push"

version-tag-push:
	git tag -a v$(VERSION) -m "Version $(VERSION)"
	git push --tags

package:
	make dist/autoplot-$(VERSION).tar.gz

dist/autoplot-$(VERSION).tar.gz:
	# TODO: one must manually update the version
	python setup.py sdist

release: dist/autoplot-$(VERSION).tar.gz
	pip install twine
	twine upload \
		-r pypi dist/autoplot-$(VERSION).tar.gz \
		&& \
	echo Uploaded to $(subst upload.,,$(URL))/project/autoplot/

# TODO: Use tox
test:
	- conda create -n $(PYTHON) python=$(PYTHONV) 2>/dev/null
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
