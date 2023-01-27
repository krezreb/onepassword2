#SHELL := /bin/bash -i

setup_dev:
	pip3 install twine sdist bdist_wheel

clean:
	@rm -rf build dist *egg-info */__pycache__ tmp

build: clean
	python3 setup.py sdist bdist_wheel

publish_py2: build
	keyring --disable && python3 -m twine upload dist/*
	make clean

local_install: clean
	pip3 uninstall -y onepassword2
	python3 setup.py install --user
	make clean

test:
	bash -i test.sh

unititests:
	python3 -m pytest tests/*py