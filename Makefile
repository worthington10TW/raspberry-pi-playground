setup:
	PYTHONPATH=$PYTHONPATH:..
	pipenv --python 3
	pipenv install

init:
	python3 -m flake8 monitor
	python3 -m flake8 test

.PHONY: test
test: init
	python3 -m pytest --pyargs test -v

.PHONY: debug
debug: init
	python3 monitor/app.py -log debug

.PHONY: run
run: init
	python3 -O monitor/app.py -log info &

.PHONY: publish
publish: init
	python3 setup.py sdist bdist_wheel

.PHONY: install-monitor
install-monitor:
	python3 -m pip install monitor-0.1.0-py3-none-any.whl --force-reinstall

