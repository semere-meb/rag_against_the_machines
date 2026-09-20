SYNC := .synced
RUFF_PREFIX := $(shell [ -e /etc/NIXOS ] && echo "" || echo "uv run ")


run: install
	uv run python src/main.py

install: $(SYNC)

$(SYNC): pyproject.toml
	which uv || pip install uv
	uv sync
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf dist/
	rm -rf $(SYNC)
	rm -rf .venv

lint: $(SYNC)
	$(RUFF_PREFIX) ruff check .
	uv run flake8 .
	uv run mypy --strict .

test: $(SYNC)
	uv run pytest -q

format:
	$(RUFF_PREFIX) ruff format .
	$(RUFF_PREFIX) ruff check --fix .

re: clean run

	
.PHONY: run cheat install clean lint test format re
