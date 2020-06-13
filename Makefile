.PHONY: install

install:
	python3 -m pip install .

package:
	python3 setup.py sdist bdist_wheel

publish:
	python3 -m twine upload dist/*

