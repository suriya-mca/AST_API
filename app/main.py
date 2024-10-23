from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# from .models import Rule
# from .schemas import RuleCreate, Rule as RuleSchema
# from .ast_logic import parse_rule, combine_rules, evaluate_rule


app = FastAPI()

@app.get("/hi")
async def home():
    return "hi"

# Tortoise ORM Configuration
register_tortoise(
    app,
    db_url="postgres://postgres:postgres-password@172.18.0.1/ast_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
