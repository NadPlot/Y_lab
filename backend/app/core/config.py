from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "REST API Меню ресторана"
DESCRIPTION = "Интенсив по Python (Y_lab University)"
VERSION = "1.0.0"
TAGS_METADATA = [
    {
        "name": "Menu",
        "description": "CRUD Menu. List Menu",
    },
    {
        "name": "Submenu",
        "description": "CRUD Submenu. List Submenu",
    },
    {
        "name": "Dishes",
        "description": "CRUD Dishes. List Dishes",
    },
]

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
