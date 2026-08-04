#!/usr/bin/env python3
"""WAHA-HI Runtime Installer - Single file, no dependencies."""

import os
from pathlib import Path

REPO = Path.home() / "downloads" / "WAHA-HI"
RUNTIME = REPO / "runtime"

FILES = {
    "runtime/__init__.py": '''"""WAHA-HI Runtime Package."""
from runtime.version import __version__
from runtime.core.engine import RuntimeEngine
__all__ = ["RuntimeEngine", "__version__"]
''',

    "runtime/version.py": '''"""Version management."""
__version__ = "0.1.0"
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_STRING = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
''',

    "runtime/constants.py": '''"""Constants for WAHA-HI Runtime."""
import os
PROJECT_NAME = "WAHA-HI"
PROJECT_SLUG = "waha-hi"
DIR_ASSETS = "assets"
DIR_AUTOMATION = "automation"
DIR_COMPANION = "companion"
DIR_CONTENT = "content"
DIR_CRM = "crm"
DIR_DEPLOY = "deploy"
DIR_DOCS = "docs"
DIR_KNOWLEDGE = "knowledge"
DIR_LOGS = "logs"
DIR_PATRIMONY = "patrimony"
DIR_RUNTIME = "runtime"
DIR_SCRIPTS = "scripts"
DIR_TESTS = "tests"
CRITICAL_DIRECTORIES = [
    DIR_ASSETS, DIR_AUTOMATION, DIR_COMPANION, DIR_CONTENT,
    DIR_CRM, DIR_DEPLOY, DIR_DOCS, DIR_KNOWLEDGE,
    DIR_LOGS, DIR_PATRIMONY, DIR_RUNTIME, DIR_SCRIPTS, DIR_TESTS,
]
RUNTIME_CACHE_DIR = "cache"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_NAME = "runtime.log"
TERMUX_PREFIX = "/data/data/com.termux"
WAHA_HOST_DEFAULT = "localhost"
WAHA_PORT_DEFAULT = 3000
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_VALIDATION_ERROR = 2
''',

    "runtime/paths.py": '''"""Path resolution."""
import os, sys
from pathlib import Path
from runtime import constants
def get_repository_root():
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent
    for parent in [current_dir] + list(current_dir.parents):
        runtime_dir = parent / constants.DIR_RUNTIME
        if runtime_dir.is_dir():
            if all((parent / d).is_dir() for d in constants.CRITICAL_DIRECTORIES[:3]):
                return parent
    current_working = Path.cwd()
    if all((current_working / d).is_dir() for d in constants.CRITICAL_DIRECTORIES[:3]):
        return current_working
    raise RuntimeError("Cannot determine repository root.")
def get_runtime_dir(): return get_repository_root() / constants.DIR_RUNTIME
def get_logs_dir(): return get_repository_root() / constants.DIR_LOGS
def get_cache_dir():
    cache = get_runtime_dir() / constants.RUNTIME_CACHE_DIR
    cache.mkdir(parents=True, exist_ok=True)
    return cache
def get_knowledge_dir(): return get_repository_root() / constants.DIR_KNOWLEDGE
def get_crm_dir(): return get_repository_root() / constants.DIR_CRM
def get_content_dir(): return get_repository_root() / constants.DIR_CONTENT
def get_companion_dir(): return get_repository_root() / constants.DIR_COMPANION
def get_automation_dir(): return get_repository_root() / constants.DIR_AUTOMATION
def get_log_file_path(): return get_logs_dir() / constants.LOG_FILE_NAME
def add_repo_to_sys_path():
    root = str(get_repository_root())
    if root not in sys.path: sys.path.insert(0, root)
''',

    "runtime/environment.py": '''"""Environment detection."""
import os, platform, sys
from runtime import constants
def is_termux():
    prefix = os.environ.get("PREFIX", "")
    if prefix.startswith(constants.TERMUX_PREFIX): return True
    if "TERMUX_VERSION" in os.environ: return True
    home = os.environ.get("HOME", "")
    if "/data/data/com.termux" in home: return True
    return False
def is_android():
    if is_termux(): return True
    if "android" in platform.uname().release.lower(): return True
    if os.path.exists("/system/build.prop"): return True
    return False
def get_python_version(): return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
def get_platform_info():
    return {
        "system": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "processor": platform.processor(),
        "python_version": get_python_version(), "is_termux": is_termux(),
        "is_android": is_android(), "prefix": os.environ.get("PREFIX", ""),
        "home": os.environ.get("HOME", ""),
    }
def check_python_version(min_major=3, min_minor=13):
    return sys.version_info.major > min_major or (sys.version_info.major == min_major and sys.version_info.minor >= min_minor)
def get_environment_summary():
    info = get_platform_info()
    env_type = "Termux (Android)" if info["is_termux"] else "Standard"
    if info["is_android"] and not info["is_termux"]: env_type = "Android (non-Termux)"
    return "\\n".join([
        f"Environment: {env_type}", f"System: {info['system']} {info['release']}",
        f"Machine: {info['machine']}", f"Python: {info['python_version']}",
        f"Prefix: {info['prefix'] or 'N/A'}",
    ])
''',

    "runtime/exceptions.py": '''"""Custom exceptions."""
class WahaHiRuntimeError(Exception): pass
class ConfigurationError(WahaHiRuntimeError): pass
class ValidationError(WahaHiRuntimeError): pass
class EnvironmentError(WahaHiRuntimeError): pass
class PathResolutionError(WahaHiRuntimeError): pass
class EngineError(WahaHiRuntimeError): pass
''',

    "runtime/logger.py": '''"""Logging configuration."""
import logging, sys
from pathlib import Path
from runtime import constants, paths
def get_logger(name="waha-hi"):
    logger = logging.getLogger(name)
    if logger.handlers: return logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=constants.LOG_FORMAT, datefmt=constants.LOG_DATE_FORMAT)
    log_file_path = paths.get_log_file_path()
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(filename=str(log_file_path), mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
def configure_root_logger(): return get_logger("waha-hi")
def log_environment_info(logger):
    from runtime import environment
    info = environment.get_platform_info()
    logger.info("Environment detected:")
    logger.info("  System: %s %s", info["system"], info["release"])
    logger.info("  Machine: %s", info["machine"])
    logger.info("  Python: %s", info["python_version"])
    logger.info("  Termux: %s", info["is_termux"])
    logger.info("  Android: %s", info["is_android"])
''',

    "runtime/config.py": '''"""Configuration management."""
import os
from pathlib import Path
from runtime import constants, paths, version
class RuntimeConfig:
    def __init__(self):
        self.project_name = constants.PROJECT_NAME
        self.project_slug = constants.PROJECT_SLUG
        self.version = version.VERSION_STRING
        self.repository_root = paths.get_repository_root()
        self.logs_dir = paths.get_logs_dir()
        self.cache_dir = paths.get_cache_dir()
        self.waha_host = os.environ.get("WAHA_HOST", constants.WAHA_HOST_DEFAULT)
        self.waha_port = int(os.environ.get("WAHA_PORT", str(constants.WAHA_PORT_DEFAULT)))
    def as_dict(self):
        return {
            "project_name": self.project_name, "project_slug": self.project_slug,
            "version": self.version, "repository_root": str(self.repository_root),
            "logs_dir": str(self.logs_dir), "cache_dir": str(self.cache_dir),
            "waha_host": self.waha_host, "waha_port": self.waha_port,
        }
    def __repr__(self):
        return f"RuntimeConfig(project={self.project_name}, version={self.version}, root={self.repository_root})"
''',

    "runtime/bootstrap.py": '''"""WAHA-HI Runtime Bootstrap."""
import sys
from runtime.core.engine import RuntimeEngine
from runtime import constants
def main():
    engine = RuntimeEngine()
    return engine.run()
if __name__ == "__main__":
    sys.exit(main())
''',

    "runtime/README.md": """# WAHA-HI Runtime\nFoundation layer for WAHA-HI.\n\n## Execution\n```bash\npython runtime/bootstrap.py\n```\n\n## Compatibility\n- Android 14/15\n- Termux\n- Python 3.13+\n- No Docker\n- No cloud dependencies\n""",

    "runtime/core/__init__.py": '''"""WAHA-HI Runtime Core."""
from runtime.core.engine import RuntimeEngine
from runtime.core.registry import ComponentRegistry
from runtime.core.loader import ModuleLoader
__all__ = ["RuntimeEngine", "ComponentRegistry", "ModuleLoader"]
''',

    "runtime/core/engine.py": '''"""RuntimeEngine for WAHA-HI."""
import sys
from pathlib import Path
from runtime import constants, exceptions
from runtime.config import RuntimeConfig
from runtime.logger import configure_root_logger, log_environment_info
from runtime import environment
from runtime.validators.filesystem import FilesystemValidator
class RuntimeEngine:
    def __init__(self):
        self.config = None
        self.logger = configure_root_logger()
        self.validator = None
        self._initialized = False
    def initialize(self):
        self.logger.info("Initializing RuntimeEngine")
        self.config = RuntimeConfig()
        self.validator = FilesystemValidator(self.config.repository_root)
        self._initialized = True
        self.logger.info("Configuration loaded: %s", self.config)
    def validate(self):
        if not self._initialized:
            raise exceptions.EngineError("Engine not initialized.")
        self.logger.info("Running validations")
        self.validator.validate_all()
        self.logger.info("All validations passed")
    def prepare_environment(self):
        self.logger.info("Preparing environment")
        if not environment.check_python_version():
            current = environment.get_python_version()
            raise exceptions.EnvironmentError(f"Python {current} is below minimum required 3.13")
        self.config.logs_dir.mkdir(parents=True, exist_ok=True)
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info("Environment prepared")
    def run(self):
        try:
            self.initialize()
            log_environment_info(self.logger)
            self.validate()
            self.prepare_environment()
            self.logger.info("RuntimeEngine completed successfully")
            return constants.EXIT_SUCCESS
        except exceptions.WahaHiRuntimeError as e:
            self.logger.error("Runtime error: %s", e)
            return constants.EXIT_FAILURE
        except Exception as e:
            self.logger.error("Unexpected error: %s", e)
            return constants.EXIT_FAILURE
    def shutdown(self):
        self.logger.info("Shutting down RuntimeEngine")
        self._initialized = False
''',

    "runtime/core/registry.py": '''"""Component registry."""
from typing import Any
class ComponentRegistry:
    def __init__(self): self._components = {}
    def register(self, name, component):
        if name in self._components: raise ValueError(f"Component '{name}' already registered")
        self._components[name] = component
    def get(self, name):
        if name not in self._components: raise KeyError(f"Component '{name}' not found")
        return self._components[name]
    def has(self, name): return name in self._components
    def list(self): return sorted(self._components.keys())
    def unregister(self, name):
        if name not in self._components: raise KeyError(f"Component '{name}' not found")
        del self._components[name]
''',

    "runtime/core/loader.py": '''"""Module loader."""
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
''',

    "runtime/validators/__init__.py": '''"""WAHA-HI Runtime Validators."""
from runtime.validators.filesystem import FilesystemValidator
from runtime.validators.metadata import MetadataValidator
from runtime.validators.knowledge import KnowledgeValidator
__all__ = ["FilesystemValidator", "MetadataValidator", "KnowledgeValidator"]
''',

    "runtime/validators/filesystem.py": '''"""Filesystem validation."""
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
''',

    "runtime/validators/metadata.py": '''"""Metadata validation."""
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
''',

    "runtime/validators/knowledge.py": '''"""Knowledge structure validation."""
from pathlib import Path
from runtime import exceptions
class KnowledgeValidator:
    REQUIRED_SUBDIRS = ["books", "faq", "glosario", "laws", "observatorio"]
    def __init__(self, knowledge_dir):
        self.knowledge_dir = Path(knowledge_dir)
        self.errors = []
    def validate_structure(self):
        all_exist = True
        for subdir in self.REQUIRED_SUBDIRS:
            if not (self.knowledge_dir / subdir).is_dir():
                self.errors.append(f"Missing knowledge subdirectory: {subdir}")
                all_exist = False
        return all_exist
    def validate_all(self):
        self.errors = []
        if not self.validate_structure():
            raise exceptions.ValidationError(f"Knowledge validation failed: {'; '.join(self.errors)}")
''',

    "runtime/utils/__init__.py": '''"""WAHA-HI Runtime Utilities."""
from runtime.utils.files import ensure_dir, read_text, write_text
from runtime.utils.yaml import load_yaml, dump_yaml
from runtime.utils.hashes import generate_id, hash_string
__all__ = ["ensure_dir", "read_text", "write_text", "load_yaml", "dump_yaml", "generate_id", "hash_string"]
''',

    "runtime/utils/files.py": '''"""File utility functions."""
from pathlib import Path
def ensure_dir(directory):
    directory.mkdir(parents=True, exist_ok=True)
    return directory
def read_text(filepath, encoding="utf-8"):
    return filepath.read_text(encoding=encoding)
def write_text(filepath, content, encoding="utf-8"):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding=encoding)
''',

    "runtime/utils/yaml.py": '''"""YAML utility functions."""
from pathlib import Path
def load_yaml(filepath):
    content = filepath.read_text(encoding="utf-8")
    return _parse_yaml(content)
def dump_yaml(data, filepath):
    yaml_text = _serialize_yaml(data)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(yaml_text, encoding="utf-8")
def _parse_yaml(content):
    lines = content.split("\\n")
    result = {}
    current_dict = result
    stack = []
    current_list = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line or line.startswith("#"): continue
        indent = len(raw_line) - len(raw_line.lstrip())
        stripped = line.lstrip()
        if stripped.startswith("- "):
            value_str = stripped[2:].strip()
            value = _parse_value(value_str)
            if current_list is None:
                current_list = []
                if stack:
                    parent_dict, _ = stack[-1]
                    last_key = list(parent_dict.keys())[-1]
                    parent_dict[last_key] = current_list
            current_list.append(value)
            continue
        current_list = None
        while stack and stack[-1][1] >= indent:
            stack.pop()
            current_dict = stack[-1][0] if stack else result
        if ":" not in stripped: continue
        colon_idx = stripped.index(":")
        key = stripped[:colon_idx].strip()
        value_str = stripped[colon_idx+1:].strip()
        if not value_str:
            new_dict = {}
            current_dict[key] = new_dict
            stack.append((current_dict, indent))
n            current_dict = new_dict
        else:
            current_dict[key] = _parse_value(value_str)
    return result
def _parse_value(value_str):
    value_str = value_str.strip()
    if not value_str or value_str.lower() in ("null", "~"): return None
    if value_str.lower() in ("true", "yes", "on"): return True
    if value_str.lower() in ("false", "no", "off"): return False
    try: return int(value_str)
    except ValueError: pass
    try: return float(value_str)
    except ValueError: pass
    if (value_str.startswith('"') and value_str.endswith('"')) or (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str
def _serialize_yaml(data, indent=0):
    spaces = "  " * indent
    if isinstance(data, dict):
        if not data: return "{}"
        lines = []
        for key, value in data.items():
            if isinstance(value, dict) and value:
                lines.append(f"{spaces}{key}:")
                lines.append(_serialize_yaml(value, indent+1))
            elif isinstance(value, list):
                lines.append(f"{spaces}{key}:")
                for item in value: lines.append(f"{spaces}- {_serialize_inline(item)}")
            else:
                lines.append(f"{spaces}{key}: {_serialize_inline(value)}")
        return "\\n".join(lines)
    return _serialize_inline(data)
def _serialize_inline(value):
    if value is None: return "null"
    if isinstance(value, bool): return "true" if value else "false"
    if isinstance(value, (int, float)): return str(value)
    if isinstance(value, str):
        if any(c in value for c in [":", "#", "\\n", '"', "'"]):
            escaped = value.replace('"', '\\\\"')
            return f'"{escaped}"'
        return value
    return str(value)
''',

    "runtime/utils/hashes.py": '''"""Hash utility functions."""
import hashlib, secrets, uuid
def generate_id(): return uuid.uuid4().hex
def hash_string(input_string, algorithm="sha256"):
    encoded = input_string.encode("utf-8")
    if algorithm == "sha256": return hashlib.sha256(encoded).hexdigest()
    elif algorithm == "sha512": return hashlib.sha512(encoded).hexdigest()
    elif algorithm == "md5": return hashlib.md5(encoded).hexdigest()
    else: raise ValueError(f"Unsupported hash algorithm: {algorithm}")
def generate_token(length=32): return secrets.token_hex(length // 2 + 1)[:length]
''',
}

def main():
    print("=" * 40)
    print("WAHA-HI Runtime Installer")
    print("=" * 40)

    for subdir in ["core", "validators", "utils"]:
        (RUNTIME / subdir).mkdir(parents=True, exist_ok=True)

    created = 0
    for filepath, content in FILES.items():
        full = REPO / filepath
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        print(f"  OK {filepath}")
        created += 1

    print(f"\nTotal: {created} files")

    import subprocess
    result = subprocess.run(
        ["python3", str(RUNTIME / "bootstrap.py")],
        cwd=str(REPO), capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr: print(result.stderr)
    print(f"Exit code: {result.returncode}")

    if result.returncode == 0:
        print("\n" + "=" * 40)
        print("SUCCESS")
        print("=" * 40)
        print(f"\nGit commands:")
        print(f"  cd {REPO}")
        print("  git add runtime/")
        print("  git commit -m 'IMPLEMENTAR 001: Runtime Foundation v0.1.0'")
    return result.returncode

if __name__ == "__main__":
    exit(main())
