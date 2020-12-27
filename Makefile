init:
	PYTHONPATH=$PYTHONPATH:..
	pip install -r requirements.txt
	flake8 .

.PHONY: test
test: init
	pytest --pyargs app -v 

.PHONY: install
install: init
	pip wheel .

.PHONY: run
run: init
	python app/app.py
