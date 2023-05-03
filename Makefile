PKG_VERSION = $(shell python setup.py --version)

build-docs:
	pip install -r requirements_doc.txt
	sphinx-build -b html docs docs/_build/html
	