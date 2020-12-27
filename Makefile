init:
	PYTHONPATH=$PYTHONPATH:..
	pip3 install -r requirements.txt
	flake8 .

.PHONY: test
test: init
	pytest --pyargs app -v 

.PHONY: install
install: init
	pip3 wheel .

.PHONY: run
run: init
	python app/app.py
