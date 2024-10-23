from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import RuleModel
from schemas import RuleCreate, RuleUpdate, RuleResponse, UserData, RulesToCombine, RuleEvaluation, RuleCombinationResponse
from ast_logic import create_rule, combine_rules, evaluate_rule


app = FastAPI()

@app.post("/api/rules")
async def create_rule_api(rule: RuleCreate):
    try:
        # Validate the rule by attempting to create an AST
        create_rule(rule.rule_string)
        # Save rule to database
        await RuleModel.create(rule_string=rule.rule_string)
        return {"message": "Rule created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid rule: {str(e)}")

@app.get("/api/rules")
async def get_rules():
    rules = await RuleModel.all()
    return [{"id": rule.id, "rule_string": rule.rule_string} for rule in rules]

@app.post("/api/combine_rules")
async def combine_rules_api(rules_to_combine: RulesToCombine):
    if len(rules_to_combine.rules) < 2:
        raise HTTPException(status_code=400, detail="At least two rules are required for combination")
    
    rule_strings = [rule['rule_string'] for rule in rules_to_combine.rules]
    try:
        combined_node = combine_rules(rule_strings)
        combined_rule_string = node_to_string(combined_node)
        return {"combined_rule": combined_rule_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rule combination error: {str(e)}")

@app.post("/api/evaluate")
async def evaluate_rules(data: UserData):
    rules = await RuleModel.all()
    if not rules:
        raise HTTPException(status_code=404, detail="No rules found")
    
    combined_rule = combine_rules([rule.rule_string for rule in rules])
    try:
        result = evaluate_rule(combined_rule, data.dict())
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Evaluation error: {str(e)}")

# Tortoise ORM Configuration
register_tortoise(
    app,
    db_url="postgres://postgres:postgres-password@172.18.0.1/ast_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
