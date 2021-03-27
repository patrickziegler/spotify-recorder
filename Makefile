install:
	pip3 install -r requirements.txt --user
	python3 setup.py install --user

develop:
	$(MAKE) venv
	bash -c "source .venv/bin/activate && python setup.py develop"

clean:
	rm -rf .venv build dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

venv:
	$(MAKE) clean
	virtualenv --python=/usr/bin/python3 .venv
	bash -c "source .venv/bin/activate && pip install -r requirements.txt"
