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
	@black --check --diff ${PY_SOURCE_FILES}
	@isort --check --diff --project=${PROJECT} ${PY_SOURCE_FILES}

format:
	@autoflake --in-place --recursive ${PY_SOURCE_FILES}
	@isort --project=${PROJECT} ${PY_SOURCE_FILES}
	@black ${PY_SOURCE_FILES}

install:
	@pip install -q .[msgpack]

test: install
	@pytest test -vv -s

bench: install
	@python benchmark/bench.py
