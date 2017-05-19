.PHONY: test clean

test:
	python3 setup.py test

lint:
	python3 setup.py flake8

clean:
	rm -rf build dist

build:
	make test
	make lint
	python3 setup.py bdist bdist_wheel

publish:
	make build
	twine dist/*
