"""Logging configuration."""
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
