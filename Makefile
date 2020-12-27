init:
	PYTHONPATH=$PYTHONPATH:..
	pip install -r requirements.txt

.PHONY: test
test: init
	pytest --pyargs app -v

.PHONY: install
install: init
	pip install .

.PHONY: run
run: init
	python app/app.py
