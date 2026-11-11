"""Configuración central de la aplicación Products API.

Inicializa Connexion, la aplicación Flask, la conexión a SQLite y las
extensiones de SQLAlchemy y Marshmallow.
"""

from pathlib import Path

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Rutas del paquete y de la raíz del proyecto
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent

# Aplicación Connexion (OpenAPI 3.0 + Swagger UI)
connex_app = connexion.FlaskApp(
    __name__,
    specification_dir=PROJECT_ROOT / "docs",
    server_args={
        "template_folder": str(PACKAGE_DIR / "templates"),
        "static_folder": str(PACKAGE_DIR / "static"),
    },
)

# Aplicación Flask subyacente
app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{PROJECT_ROOT / 'products.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)
