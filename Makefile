#SHELL := /bin/bash -i

setup_dev:
	pip3 install twine sdist bdist_wheel

clean:
	rm -rf build dist *egg-info */__pycache__


build: clean
	python3 setup.py sdist bdist_wheel

publish_py2: build
	python3 -m twine upload dist/*

local_install: clean
	pip3 uninstall -y onepassword2
	python3 setup.py install --user

test:
	bash -i test.sh