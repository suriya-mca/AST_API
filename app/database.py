from tortoise import Tortoise


TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:postgres-password@172.18.0.1/ast_db"
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()
