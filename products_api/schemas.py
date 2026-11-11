"""Esquemas de Marshmallow para serializar y deserializar productos."""

from products_api.config import db, ma
from products_api.models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    """Esquema JSON basado automáticamente en el modelo ``Product``."""

    class Meta:
        model = Product
        load_instance = True
        sqla_session = db.session


# Instancias reutilizables del esquema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
