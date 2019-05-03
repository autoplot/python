#PYTHONV=2.7
PYTHONV=3.6

PYTHON=python$(PYTHONV)

test:
	#- conda create -n $(PYTHON) python=$(PYTHONV)
	# you need to run the above command manually.
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
