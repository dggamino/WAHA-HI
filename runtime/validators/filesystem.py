"""Filesystem validation."""
import os
from pathlib import Path
from runtime import constants, exceptions
class FilesystemValidator:
    def __init__(self, root):
        self.root = Path(root)
        self.errors = []
    def validate_directories(self):
        all_exist = True
        for dirname in constants.CRITICAL_DIRECTORIES:
            if not (self.root / dirname).is_dir():
                self.errors.append(f"Missing directory: {dirname}")
                all_exist = False
        return all_exist
    def validate_permissions(self):
        all_valid = True
        if not os.access(self.root, os.R_OK):
            self.errors.append(f"No read permission: {self.root}")
            all_valid = False
        logs_dir = self.root / constants.DIR_LOGS
        logs_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(logs_dir, os.W_OK):
            self.errors.append(f"No write permission: {logs_dir}")
            all_valid = False
        cache_dir = self.root / constants.DIR_RUNTIME / constants.RUNTIME_CACHE_DIR
        cache_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(cache_dir, os.W_OK):
            self.errors.append(f"No write permission: {cache_dir}")
            all_valid = False
        return all_valid
    def validate_all(self):
        self.errors = []
        dirs_ok = self.validate_directories()
        perms_ok = self.validate_permissions()
        if not (dirs_ok and perms_ok):
            raise exceptions.ValidationError(f"Filesystem validation failed: {'; '.join(self.errors)}")
