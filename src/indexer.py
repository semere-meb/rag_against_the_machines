import os
from pathlib import Path
from typing import Generator


def get_files_by_extension(
    ext: str, dir: Path = Path(".")
) -> Generator[Path, None, None]:
    files: Generator[Path, None, None] = dir.rglob(f"./*.{ext}")
    return files


def get_all_files() -> list[Path]:
    raw_dir = Path("data/raw/vllm-0.10.1/")

    if not (raw_dir.exists() and raw_dir.is_dir()):
        print("WARNING: raw directory not")
        os._exit(1)

    python_files = get_files_by_extension("py", raw_dir)
    markdown_files = get_files_by_extension("md", raw_dir)

    for file in python_files:
        print(file)

    return [*python_files, *markdown_files]
