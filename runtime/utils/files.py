"""File utility functions."""
from pathlib import Path
def ensure_dir(directory):
    directory.mkdir(parents=True, exist_ok=True)
    return directory
def read_text(filepath, encoding="utf-8"):
    return filepath.read_text(encoding=encoding)
def write_text(filepath, content, encoding="utf-8"):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding=encoding)
