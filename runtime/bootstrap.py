"""WAHA-HI Runtime Bootstrap."""
import sys
from pathlib import Path
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
from runtime.core.engine import RuntimeEngine
from runtime import constants
def main():
    engine = RuntimeEngine()
    return engine.run()
if __name__ == "__main__":
    sys.exit(main())
