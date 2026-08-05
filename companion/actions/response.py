"""
companion/actions/response.py

WAHA-HI ActionResponseBuilder — Sprint 031

Responsabilidad:
  - Construir respuestas estructuradas para el Pipeline.
  - Acumular contenido de múltiples acciones.
  - Generar output compatible con Responder (Sprint existente).

Diseño:
  - Builder pattern para construcción incremental.
  - Output serializable a dict para integración con Pipeline.
  - Soporte para texto, metadata, sugerencias, y attachments.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ActionResponseBuilder:
    """
    Builder para respuestas del Companion Engine.
    
    Permite construir respuestas incrementalmente
    a partir de resultados de múltiples acciones.
    """
    
    text_parts: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 1.0
    
    def add_text(self, text: str, separator: str = "\n") -> "ActionResponseBuilder":
        """Agrega texto a la respuesta."""
        if text:
            self.text_parts.append(text)
        return self
    
    def set_text(self, text: str) -> "ActionResponseBuilder":
        """Establece el texto completo (reemplaza partes)."""
        self.text_parts = [text] if text else []
        return self
    
    def add_metadata(self, **kwargs: Any) -> "ActionResponseBuilder":
        """Agrega pares clave-valor a metadata."""
        self.metadata.update(kwargs)
        return self
    
    def set_metadata(self, metadata: Dict[str, Any]) -> "ActionResponseBuilder":
        """Establece metadata completa."""
        self.metadata = dict(metadata)
        return self
    
    def add_suggestion(self, suggestion: str) -> "ActionResponseBuilder":
        """Agrega una sugerencia de follow-up."""
        if suggestion and suggestion not in self.suggestions:
            self.suggestions.append(suggestion)
        return self
    
    def add_suggestions(self, suggestions: List[str]) -> "ActionResponseBuilder":
        """Agrega múltiples sugerencias."""
        for s in suggestions:
            self.add_suggestion(s)
        return self
    
    def add_attachment(self, type_: str, content: Any, **meta: Any) -> "ActionResponseBuilder":
        """Agrega un attachment estructurado."""
        self.attachments.append({
            "type": type_,
            "content": content,
            "meta": meta,
        })
        return self
    
    def set_confidence(self, confidence: float) -> "ActionResponseBuilder":
        """Establece score de confianza."""
        self.confidence = max(0.0, min(1.0, confidence))
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Construye la respuesta final.
        
        Returns:
            Dict serializable compatible con Pipeline/Responder.
        """
        text = self._join_text()
        return {
            "type": "companion_response",
            "text": text,
            "metadata": {
                **self.metadata,
                "confidence": self.confidence,
                "timestamp": time.time(),
                "has_attachments": len(self.attachments) > 0,
            },
            "suggestions": self.suggestions,
            "attachments": self.attachments,
        }
    
    def _join_text(self) -> str:
        """Une las partes de texto."""
        return "\n".join(p for p in self.text_parts if p)
    
    def is_empty(self) -> bool:
        """Verifica si la respuesta está vacía."""
        return not self.text_parts and not self.attachments
    
    @classmethod
    def from_action_results(cls, results: List[Any]) -> "ActionResponseBuilder":
        """
        Factory: construye builder a partir de ActionResults.
        
        Args:
            results: Lista de ActionResult o dicts con 'output'.
        """
        builder = cls()
        for result in results:
            if hasattr(result, "output") and result.output:
                if isinstance(result.output, str):
                    builder.add_text(result.output)
                elif isinstance(result.output, dict) and "text" in result.output:
                    builder.add_text(result.output["text"])
                    if "metadata" in result.output:
                        builder.add_metadata(**result.output["metadata"])
                    if "suggestions" in result.output:
                        builder.add_suggestions(result.output["suggestions"])
            elif isinstance(result, dict) and result.get("output"):
                out = result["output"]
                if isinstance(out, str):
                    builder.add_text(out)
                elif isinstance(out, dict) and "text" in out:
                    builder.add_text(out["text"])
        return builder
    
    def __repr__(self) -> str:
        return f"<ActionResponseBuilder text_len={len(self._join_text())}>"
