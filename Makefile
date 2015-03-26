default:
	@echo "'make check'" to run tests
	@echo "'make lint'" to run flake8 checks

.PHONY: check
check:
	nosetests -v pygesture

.PHONY: lint
lint:
	flake8 --config=tools/flake8.cfg \
		pygesture \
		examples/analyze \
		examples/process
