install:
	uv pip install -e .[dev]

run:
	uv run blast_radius/main.py

test:
	uv run pytest 