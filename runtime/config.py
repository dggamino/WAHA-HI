"""Configuration management."""
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
