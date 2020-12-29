init:
	PYTHONPATH=$PYTHONPATH:..
	pip3 install -r requirements.txt
	pip3 install -e .
	python3 -m flake8 src
	python3 -m flake8 test

.PHONY: test
test: init
	python3 -m pytest --pyargs test -v

.PHONY: install
install: init
	pip3 install -e .

.PHONY: run
run: init
	python3 src/app.py

