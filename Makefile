PY_SOURCE_FILES=numbin test benchmark
PROJECT=numbin

.PHONY: test doc

build: clean
	@uv build

publish: build
	@uv publish

clean:
	@-rm -rf build/ dist/ .eggs/ site/ *.egg-info .pytest_cache .mypy_cache
	@-find . -name '*.pyc' -type f -exec rm -rf {} +
	@-find . -name '__pycache__' -exec rm -rf {} +

dev:
	@uv sync --group dev

lint:
	@uv run -- ruff check ${PY_SOURCE}
	@uv run -- ruff format --check ${PY_SOURCE}

format:
	@uv run -- ruff check --fix ${PY_SOURCE}
	@uv run -- ruff format ${PY_SOURCE}

install:
	@uv sync --extra msgpack

test: install dev
	@uv run -- pytest test -vv -s

bench: install
	@uv run benchmark/bench.py
