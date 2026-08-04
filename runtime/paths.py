"""Path resolution."""
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
