# companion/flows/landing_flow.py
# HEREDITARIA™ OS — Landing Context Flow

import json
from pathlib import Path


class LandingFlow:
    """Detecta si el usuario viene de una landing y enruta al libro correspondiente."""

    def __init__(self):
        self.landings = self._load_landings()
        self.landing_keywords = self._build_keyword_index()

    def _load_landings(self):
        paths = [
            Path(__file__).parent.parent.parent / "landings" / "landings.json",
            Path(__file__).parent.parent / "landings" / "landings.json",
            Path("landings/landings.json"),
        ]
        for p in paths:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
        return {"landings": [], "categories": {}}

    def _build_keyword_index(self):
        index = {}
        for landing in self.landings.get("landings", []):
            for kw in landing.get("keywords", []):
                kw_lower = kw.lower()
                if kw_lower not in index:
                    index[kw_lower] = []
                index[kw_lower].append(landing)
        return index

    def detect_landing_context(self, text: str):
        if not text:
            return None
        text_lower = text.lower()
        scores = {}
        for kw, landings in self.landing_keywords.items():
            if kw in text_lower:
                for landing in landings:
                    lid = landing["id"]
                    scores[lid] = scores.get(lid, 0) + len(kw)
        if not scores:
            return None
        best_id = max(scores, key=scores.get)
        for landing in self.landings.get("landings", []):
            if landing["id"] == best_id:
                return landing
        return None

    def get_book_recommendation(self, landing: dict):
        book_id = landing.get("book_id")
        book_title = landing.get("book_title")
        category = landing.get("category")

        if not book_id:
            return {
                "type": "text",
                "content": (
                    f"Veo que llegaste desde *{landing['display_name']}*.\n\n"
                    f"📚 Tenemos toda la *Biblioteca HEREDITARIA™* disponible.\n"
                    f"Escribe *libros* para ver el catálogo completo."
                )
            }

        cat_info = self.landings.get("categories", {}).get(category, {})

        return {
            "type": "text",
            "content": (
                f"Veo que llegaste desde *{landing['display_name']}*.\n\n"
                f"📖 Te recomiendo leer: *{book_title}*\n"
                f"Categoría: {cat_info.get('display', category)}\n\n"
                f"Escribe *{book_id.lower()}* o *{landing['keywords'][0]}* para acceder al contenido."
            ),
            "landing_id": landing["id"],
            "book_id": book_id,
            "category": category
        }

    def process(self, text: str, session_context: dict = None):
        landing = self.detect_landing_context(text)
        if landing:
            return self.get_book_recommendation(landing)
        return None


_landing_flow = None

def get_landing_flow():
    global _landing_flow
    if _landing_flow is None:
        _landing_flow = LandingFlow()
    return _landing_flow
