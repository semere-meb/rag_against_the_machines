from enum import Enum
from itertools import chain
from pathlib import Path

from pydantic import BaseModel

SUFFIXES: set[str] = {"py", "md"}
RAW_DIR: str = "data/raw/vllm-0.10.1/"
EXCLUDED_DIRS: set[str] = {".venv", ".eggs", "eggs", "__pycache__"}


class IndexError(Exception):
    """
    An Error during intake.
    """


class FileType(Enum):
    PY = ".py"
    MD = ".md"


class File(BaseModel):
    path: Path
    content: str
    type: FileType


class Indexer:
    def get_all_paths(self) -> list[Path]:
        """
        Walks through the entire repo and returns paths of files.
        """
        raw_dir: Path = Path(RAW_DIR)

        # stop if `raw_dir` doesn't exist
        if not (raw_dir.exists() and raw_dir.is_dir()):
            raise IndexError("raw directory not found")

        # convert to absolute path
        raw_dir = raw_dir.absolute()

        # walk and collect files
        paths = chain.from_iterable(
            raw_dir.rglob(f"*.{suffix}") for suffix in SUFFIXES
        )

        return list(paths)

    def filter_paths(self, paths: list[Path]) -> list[Path]:
        """
        filters excluded files.
        """
        filtered_paths = []

        for path in paths:
            if not path.is_file():
                continue
            if EXCLUDED_DIRS.intersection(path.parts):
                continue
            filtered_paths.append(path)

        return filtered_paths

    def build_file_list(self, paths: list[Path]) -> list[File]:
        """
        builds a list of read files with their content and type.
        """
        files = []

        for path in paths:
            try:
                with open(path, encoding="utf-8", newline="") as f:
                    content = f.read()
                    type = FileType(path.suffix)

                    file = File(path=path, content=content, type=type)
                    files.append(file)
            except OSError:
                print(f"Warning: Error during reading {path}, skipped.")

        return files
