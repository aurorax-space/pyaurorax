.PHONY: install update dev docs clean test

install:
	poetry install

update upgrade:
	poetry update

dev:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	~/.poetry/bin/poetry self update
	~/.poetry/bin/poetry completions bash > completions.out
	sudo cp completions.out /etc/bash_completion.d/poetry.bash-completion
	rm completions.out

docs:
	cd docsource && ${MAKE} github

clean:
	@rm -rf pyaurorax.egg-info build dist

test:
	flake8 aurorax
	python tests/test_aurorax.py

