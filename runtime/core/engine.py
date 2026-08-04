"""RuntimeEngine for WAHA-HI."""
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
