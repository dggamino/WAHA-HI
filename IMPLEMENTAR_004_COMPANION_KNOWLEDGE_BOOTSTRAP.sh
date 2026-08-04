#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 004 — Companion Knowledge Interface v0.1.0 ==="

mkdir -p companion/adapters


touch companion/adapters/__init__.py


cat > companion/adapters/knowledge.py <<'EOF'
"""
Knowledge Adapter

Punto único de acceso entre Companion
y Knowledge Layer.
"""


from knowledge.books.catalog import catalog


def get_books():

    return catalog()


def find_book(book_id):

    books = get_books()

    for book in books:

        if book["id"] == book_id:
            return book

    return None
EOF


cat > companion/adapters/__init__.py <<'EOF'
"""
Adapters layer.
"""
EOF


cat > companion/flows/books.py <<'EOF'
from companion.adapters.knowledge import get_books


def handle(context):

    context.update(
        "flow",
        "books"
    )

    books = get_books()

    titles = [
        book["title"]
        for book in books
    ]

    return {

        "type": "text",

        "content":
        "Libros HEREDITARIA disponibles: "
        + ", ".join(titles)

    }
EOF


echo ""
echo "=== VALIDACION INTERFACE ==="

python3 - <<'EOF'

from companion.engine import process

result = process(
    "Quiero conocer los libros HEREDITARIA"
)

print(result)

EOF


echo ""
echo "=== IMPLEMENTAR 004 COMPLETADO ==="
