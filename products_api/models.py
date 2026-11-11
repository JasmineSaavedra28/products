"""Modelo de base de datos para los productos."""

from datetime import datetime

from products_api.config import db


class Product(db.Model):
    """Representa un producto almacenado en la tabla ``product``."""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Product {self.nombre!r}>"
