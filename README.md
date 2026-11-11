# Products API

API RESTful para administrar un catálogo de productos, desarrollada con **Flask**, **Connexion**, **SQLAlchemy**, **Marshmallow** y **SQLite**, siguiendo la arquitectura del tutorial *People*, adaptada al dominio de Productos.

## Características

- Contrato **OpenAPI 3.0** en `docs/swagger.yml`.
- Interfaz interactiva **Swagger UI** en `/api/ui`.
- Persistencia local en SQLite (`products.db`).
- Serialización y deserialización JSON con Marshmallow.
- Operaciones CRUD completas.
- Búsqueda de productos por nombre único.
- Actualización automática del campo `timestamp` en cada modificación.

## Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje base |
| Flask | Framework web |
| Connexion 3 | Enrutamiento a partir de OpenAPI 3.0 y Swagger UI |
| Flask-SQLAlchemy | ORM y persistencia |
| Flask-Marshmallow | Serialización / deserialización |
| marshmallow-sqlalchemy | Integración entre Marshmallow y SQLAlchemy |
| SQLite | Base de datos local |
| Uvicorn | Servidor ASGI usado por Connexion 3 |

> **Nota:** Connexion 3 ejecuta la aplicación mediante Uvicorn porque su núcleo es ASGI. `python app.py` levanta el servidor en el puerto `8000`.

## Estructura del proyecto

```text
products/
├── app.py                       # Entrada: API, Swagger UI y página principal
├── products_api/                # Código de la aplicación
│   ├── __init__.py
│   ├── config.py                # Connexion, Flask, SQLAlchemy y Marshmallow
│   ├── models.py                # Modelo Product (tabla product)
│   ├── schemas.py               # ProductSchema de Marshmallow
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── products.py          # read_all, read_one, create, update, delete
│   ├── static/
│   │   └── css/
│   │       └── home.css         # Estilos de la página principal
│   └── templates/
│       └── home.html            # Catálogo HTML de productos
├── docs/
│   └── swagger.yml              # Especificación OpenAPI 3.0
├── scripts/
│   ├── __init__.py
│   └── build_database.py        # Crea products.db y carga 3 productos
├── requirements.txt             # Dependencias del proyecto
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd products
```

### 2. Crear y activar un entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

```bash
python scripts/build_database.py
```

Este script crea la tabla `product` y carga tres productos iniciales. Es idempotente: si se ejecuta varias veces, no duplica los registros existentes.

> Ejecútalo siempre desde la raíz del proyecto para que se resuelvan los imports del paquete `products_api`.

### 5. Ejecutar la API

```bash
python app.py
```

Servidor disponible en:

- Página principal: <http://localhost:8000/>
- API: <http://localhost:8000/api/products>
- Swagger UI: <http://localhost:8000/api/ui>

## Endpoints

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| `GET` | `/api/products` | Lista todos los productos | `200` |
| `POST` | `/api/products` | Crea un producto | `201`, `406` |
| `GET` | `/api/products/{nombre}` | Obtiene un producto por nombre | `200`, `404` |
| `PUT` | `/api/products/{nombre}` | Actualiza marca y precio | `200`, `404` |
| `DELETE` | `/api/products/{nombre}` | Elimina un producto | `200`, `404` |

Los nombres con espacios deben codificarse en la URL, por ejemplo:

```text
/api/products/Laptop%20Pro%2015
```

## Modelo de datos

Tabla `product`:

| Campo | Tipo | Restricciones |
|---|---|---|
| `id` | Integer | Primary Key, autoincremental |
| `nombre` | String(100) | Obligatorio, único |
| `marca` | String(100) | Obligatorio |
| `precio` | Float | Obligatorio |
| `timestamp` | DateTime | `datetime.utcnow`, se actualiza en modificaciones |

## Ejemplos de uso

> Los ejemplos usan `curl`. En Windows puedes ejecutarlos desde Git Bash o usando `curl.exe` en PowerShell.

### Listar productos

```bash
curl http://localhost:8000/api/products
```

Respuesta:

```json
[
  {
    "id": 1,
    "marca": "TechNova",
    "nombre": "Laptop Pro 15",
    "precio": 1499.99,
    "timestamp": "2026-11-11T15:16:42.037637"
  }
]
```

### Crear un producto

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Tablet Z", "marca": "TechNova", "precio": 399.99}'
```

Si el nombre ya existe, la API responde `406 Not Acceptable`.

### Consultar un producto

```bash
curl http://localhost:8000/api/products/Laptop%20Pro%2015
```

### Actualizar un producto

```bash
curl -X PUT http://localhost:8000/api/products/Laptop%20Pro%2015 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Laptop Pro 15", "marca": "TechNova", "precio": 1299.99}'
```

> `nombre` identifica al producto en la ruta y no se modifica. El cuerpo debe incluir los tres campos requeridos por el esquema OpenAPI.

### Eliminar un producto

```bash
curl -X DELETE http://localhost:8000/api/products/Tablet%20Z
```

## Decisiones de diseño

- `nombre` es la clave única de búsqueda, equivalente a `lname` en el tutorial *People*.
- `PUT` actualiza `marca` y `precio`; el nombre de la ruta se conserva para no romper la clave única.
- `timestamp` se genera automáticamente y se actualiza con `onupdate=datetime.utcnow`.
- `build_database.py` usa un contexto de aplicación porque Flask-SQLAlchemy 3.x lo requiere.
- La base `products.db` se genera localmente y está incluida en `.gitignore`.

## Notas sobre Connexion 3

El tutorial original usa Connexion 2, que registra las rutas sobre la app Flask y se ejecuta con el servidor de desarrollo de Flask. Connexion 3 cambió a una arquitectura ASGI:

```text
Uvicorn → ConnexionMiddleware → Flask → controlador de products.py
```

Por eso:

- Se usa `connexion.FlaskApp` en lugar de `connexion.App`.
- El servidor se levanta con Uvicorn.
- Swagger UI se publica en `/api/ui` mediante `SwaggerUIOptions`.

En producción se puede ejecutar directamente con un servidor ASGI:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Subir el proyecto a GitHub


`products.db` está ignorado por Git. Se regenera con:

```bash
python scripts/build_database.py
```

Para incluir la base de datos, puedes forzarla:

```bash
git add -f products.db
```

## Autor

Proyecto académico de Web API Flask SQLite.
