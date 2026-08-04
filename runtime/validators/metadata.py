"""Metadata validation."""
from pathlib import Path
from runtime import exceptions
class MetadataValidator:
    def __init__(self, root):
        self.root = Path(root)
        self.errors = []
    def validate_version_file(self):
        version_file = self.root / "runtime" / "version.py"
        if not version_file.is_file():
            self.errors.append("Missing runtime/version.py")
            return False
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("version", version_file)
            if spec is None or spec.loader is None:
                self.errors.append("Cannot load version.py")
                return False
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if not hasattr(module, "__version__"):
                self.errors.append("version.py missing __version__")
                return False
            return True
        except Exception as e:
            self.errors.append(f"version.py error: {e}")
            return False
    def validate_all(self):
        self.errors = []
        if not self.validate_version_file():
            raise exceptions.ValidationError(f"Metadata validation failed: {'; '.join(self.errors)}")
