"""Constants for WAHA-HI Runtime."""
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
