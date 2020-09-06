.PHONY: install update dev clean test publish

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

clean:
	@rm -rf pyaurorax.egg-info build dist

test:
	find . -type f -name '*.py' -exec sed -i -e "s/\r//g" {} \; 
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	pytest

publish:
	${MAKE} test
	poetry build
	poetry publish
	${MAKE} clean
