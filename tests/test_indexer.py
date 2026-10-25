from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

from src.indexer import (
    File,
    FileType,
    Indexer,
    IndexError,
)


def test_file_type_enum() -> None:
    """Test FileType enum has correct extensions."""
    assert FileType.PY.value == ".py"
    assert FileType.MD.value == ".md"


def test_file_model() -> None:
    """Test Pydantic File model initialization."""
    path = Path("test.py")
    file_obj = File(path=path, content="print('hi')", type=FileType.PY)
    assert file_obj.path == path
    assert file_obj.content == "print('hi')"
    assert file_obj.type == FileType.PY


def test_indexer_get_all_paths_missing_dir(monkeypatch: MonkeyPatch) -> None:
    """Test get_all_paths raises IndexError when RAW_DIR does not exist."""
    import src.indexer as indexer_module

    monkeypatch.setattr(indexer_module, "RAW_DIR", "nonexistent_directory_abc")
    indexer = Indexer()
    with pytest.raises(IndexError, match="raw directory not found"):
        indexer.get_all_paths()


def test_indexer_filter_paths(tmp_path: Path) -> None:
    """
    Test filter_paths correctly filters out non-files and excluded
    directories.
    """
    indexer = Indexer()

    # Create valid file
    valid_file = tmp_path / "valid.py"
    valid_file.write_text("x = 1")

    # Create file inside an excluded directory
    excluded_dir = tmp_path / "__pycache__"
    excluded_dir.mkdir()
    excluded_file = excluded_dir / "cached.py"
    excluded_file.write_text("y = 2")

    # Create a directory path in the list
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    paths = [valid_file, excluded_file, subdir]
    filtered = indexer.filter_paths(paths)

    assert valid_file in filtered
    assert excluded_file not in filtered
    assert subdir not in filtered


def test_indexer_build_file_list(tmp_path: Path) -> None:
    """
    Test build_file_list reads file contents and constructs File models
    correctly.
    """
    indexer = Indexer()

    py_file = tmp_path / "main.py"
    py_file.write_text("import sys\n", encoding="utf-8")

    md_file = tmp_path / "README.md"
    md_file.write_text("# Title\n", encoding="utf-8")

    files = indexer.build_file_list([py_file, md_file])

    assert len(files) == 2
    assert files[0].path == py_file
    assert files[0].content == "import sys\n"
    assert files[0].type == FileType.PY

    assert files[1].path == md_file
    assert files[1].content == "# Title\n"
    assert files[1].type == FileType.MD


def test_indexer_build_file_list_io_error(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """Test build_file_list handles read errors gracefully without crashing."""
    indexer = Indexer()
    # Passing a directory instead of a file causes an OSError when opened
    files = indexer.build_file_list([tmp_path])

    assert len(files) == 0
    captured = capsys.readouterr()
    assert "Warning: Error during reading" in captured.out
