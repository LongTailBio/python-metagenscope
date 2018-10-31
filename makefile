.PHONY: clean lint dev package

clean:
	rm -rf dist/*

lint:
	pylint --rcfile=.pylintrc metagenscope_cli -f parseable -r n && \
	pycodestyle metagenscope_cli --max-line-length=120 && \
	pydocstyle metagenscope_cli

dev:
	pip install -r requirements.txt

package:
	python setup.py sdist
	python setup.py bdist_wheel
