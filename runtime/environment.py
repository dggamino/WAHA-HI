"""Environment detection."""
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
    return "\n".join([
        f"Environment: {env_type}", f"System: {info['system']} {info['release']}",
        f"Machine: {info['machine']}", f"Python: {info['python_version']}",
        f"Prefix: {info['prefix'] or 'N/A'}",
    ])
