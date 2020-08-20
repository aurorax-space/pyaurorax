.PHONY: install

aurorax-test:
	python3 tests/test_api.py

doc-test:
	cd docsource
	make github

install:
	python3 -m pip install .

package:
	python3 setup.py sdist bdist_wheel

publish:
	python3 -m twine upload dist/*

