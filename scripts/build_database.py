"""Inicializa la base de datos SQLite y carga productos de prueba.

Ejecutar desde la raíz del proyecto:

    python scripts/build_database.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from products_api.config import app, db  # noqa: E402
from products_api.models import Product  # noqa: E402

PRODUCTS_DATA = [
    {"nombre": "Laptop Pro 15", "marca": "TechNova", "precio": 1499.99},
    {"nombre": "Smartphone X2", "marca": "MovilMax", "precio": 799.50},
    {"nombre": "Auriculares AirSound", "marca": "SoundWave", "precio": 89.90},
]


def build_database():
    """Crea la tabla ``product`` y agrega los datos iniciales si no existen."""
    # Flask-SQLAlchemy 3.x requiere un contexto de aplicación.
    with app.app_context():
        db.create_all()

        for item in PRODUCTS_DATA:
            exists = (
                Product.query.filter(Product.nombre == item["nombre"]).one_or_none()
            )
            if exists is None:
                db.session.add(Product(**item))

        db.session.commit()

        total = Product.query.count()

    print(f"Base de datos products.db lista. Productos registrados: {total}")


if __name__ == "__main__":
    build_database()
