import os


def _parse_frontmatter(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body
    return {}, content


def get_chapter(chapters_path, chapter_number):
    # __file__ = knowledge/books/loader.py
    # Queremos llegar a ~/WAHA-HI, que es dos niveles arriba de knowledge/books/
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.join(base_dir, chapters_path)

    if not os.path.isdir(full_path):
        return None

    files = sorted(f for f in os.listdir(full_path) if f.endswith(".md"))
    capitulos = []
    for fname in files:
        fm, body = _parse_frontmatter(os.path.join(full_path, fname))
        if fm.get("tipo") == "capitulo":
            capitulos.append((fname, fm, body))

    if 1 <= chapter_number <= len(capitulos):
        fname, fm, body = capitulos[chapter_number - 1]
        return {"seccion": fm.get("seccion", ""), "body": body}
    return None
