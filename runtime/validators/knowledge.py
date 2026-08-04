"""Knowledge structure validation."""
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
