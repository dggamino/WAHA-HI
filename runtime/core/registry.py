"""Component registry."""
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
