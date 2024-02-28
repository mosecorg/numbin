PY_SOURCE_FILES=numbin test benchmark
PROJECT=numbin

.PHONY: test doc

build: clean
	@python -m build

clean:
	@-rm -rf build/ dist/ .eggs/ site/ *.egg-info .pytest_cache .mypy_cache
	@-find . -name '*.pyc' -type f -exec rm -rf {} +
	@-find . -name '__pycache__' -exec rm -rf {} +

dev:
	@pip install -q .[dev]

lint:
	@ruff check ${PY_SOURCE_FILES}

format:
	@ruff check --fix ${PY_SOURCE_FILES}
	@ruff format ${PY_SOURCE_FILES}

install:
	@pip install -q .[msgpack]

test: install
	@pytest test -vv -s

bench: install
	@python benchmark/bench.py
