SYNC := .synced


install: $(SYNC)

$(SYNC): pyproject.toml
	@if ! command -v uv >/dev/null;then pip install uv; fi
	uv sync
	@if ! [ -d data/raw/vllm-0.10.1 ];then unzip ./data/vllm-0.10.1.zip -d ./data/raw/; fi
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf dist/
	rm -rf $(SYNC)

fclean: clean
	rm -rf .venv $(SYNC)
	uv clean

lint: $(SYNC)
	ruff check .
	uv run flake8 .
	uv run mypy --strict .

test: $(SYNC)
	uv run pytest -q

format:
	ruff format .
	ruff check --fix .

re: clean run install

	
.PHONY: run install clean lint test format re
