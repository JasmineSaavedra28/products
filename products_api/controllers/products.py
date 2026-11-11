"""Controlador de la API de productos.

Connexion invoca estas funciones a partir de las operaciones declaradas en
``docs/swagger.yml``.
"""

from flask import abort, make_response

from products_api.config import db
from products_api.models import Product
from products_api.schemas import product_schema, products_schema


def read_all():
    """Retorna la lista completa de productos."""
    products = Product.query.all()
    return products_schema.dump(products)


def read_one(nombre):
    """Retorna un producto buscado por su nombre o 404 si no existe."""
    product = Product.query.filter(Product.nombre == nombre).one_or_none()

    if product is not None:
        return product_schema.dump(product)

    abort(404, f"Producto con nombre {nombre} no encontrado")


def create(product):
    """Crea un producto nuevo o retorna 406 si el nombre ya está registrado."""
    nombre = product.get("nombre")
    existing_product = Product.query.filter(Product.nombre == nombre).one_or_none()

    if existing_product is None:
        new_product = product_schema.load(product, session=db.session)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product), 201

    abort(406, f"El producto con nombre {nombre} ya existe")


def update(nombre, product):
    """Actualiza marca y precio de un producto existente.

    El nombre es la clave de búsqueda de la ruta, por lo que no se modifica.
    Retorna 404 si el producto no existe.
    """
    existing_product = Product.query.filter(Product.nombre == nombre).one_or_none()

    if existing_product is not None:
        update_product = product_schema.load(product, session=db.session)
        existing_product.marca = update_product.marca
        existing_product.precio = update_product.precio
        db.session.merge(existing_product)
        db.session.commit()
        return product_schema.dump(existing_product), 200

    abort(404, f"Producto con nombre {nombre} no encontrado")


def delete(nombre):
    """Elimina un producto existente o retorna 404 si no existe."""
    existing_product = Product.query.filter(Product.nombre == nombre).one_or_none()

    if existing_product is not None:
        db.session.delete(existing_product)
        db.session.commit()
        return make_response(f"Producto {nombre} eliminado exitosamente", 200)

    abort(404, f"Producto con nombre {nombre} no encontrado")
