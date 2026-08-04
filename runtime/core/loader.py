"""Module loader."""
import importlib.util, sys
from pathlib import Path
from types import ModuleType
class ModuleLoader:
    def __init__(self): self.loaded = {}
    def load_from_path(self, module_path, module_name=None):
        if not module_path.is_file(): raise ImportError(f"Module path not found: {module_path}")
        name = module_name or module_path.stem
        if name in self.loaded: return self.loaded[name]
        spec = importlib.util.spec_from_file_location(name, module_path)
        if spec is None or spec.loader is None: raise ImportError(f"Cannot create spec for: {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        self.loaded[name] = module
        return module
    def load_package(self, package_path, package_name):
        if not package_path.is_dir(): raise ImportError(f"Package path not found: {package_path}")
        init_file = package_path / "__init__.py"
        if not init_file.exists(): raise ImportError(f"Package missing __init__.py: {package_path}")
        return self.load_from_path(init_file, package_name)
