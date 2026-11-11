"""Punto de entrada de la API de Productos."""

from connexion.options import SwaggerUIOptions
from flask import render_template

from products_api import config
from products_api.models import Product

app = config.connex_app

# Carga el contrato OpenAPI y publica Swagger UI en http://localhost:8000/api/ui
app.add_api(
    "swagger.yml",
    swagger_ui_options=SwaggerUIOptions(
        swagger_ui_path="/api/ui",
        swagger_ui_config={"persistAuthorization": True},
    ),
)


@app.route("/")
def home():
    """Muestra una página con el catálogo de productos."""
    products = Product.query.order_by(Product.id).all()
    return render_template("home.html", products=products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
