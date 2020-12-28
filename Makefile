init:
	PYTHONPATH=$PYTHONPATH:..
	pip3 install -r requirements.txt --user
	flake8 .

.PHONY: test
test: init
	python -m pytest --pyargs app -v 

.PHONY: install
install: init
	pip3 wheel .

.PHONY: run
run: init
	python3 app/app.py
