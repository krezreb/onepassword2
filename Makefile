#SHELL := /bin/bash -i

setup_dev:
	pip3 install twine sdist bdist_wheel

publish_py2:
	rm -rf dist build
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

local_install:
	pip3 uninstall onepassword2
	python3 setup.py install
test:
	bash -i test.sh