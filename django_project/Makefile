clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'Untitled.ipynb' -delete
	rm -rf '.ipynb_checkpoints'
	rm -rf '../.pytest_cache'
	rm -rf '../htmlcov'

test: clean
	pytest tests/
