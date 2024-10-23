from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class RuleCreate(BaseModel):
    """Schema for creating a new rule"""
    rule_string: str

class RuleUpdate(BaseModel):
    """Schema for updating an existing rule"""
    rule_string: Optional[str] = None
    is_active: Optional[bool] = None

class RuleResponse(BaseModel):
    """Schema for rule response"""
    id: int
    rule_string: str
    is_active: bool
    created_at: datetime

class UserData(BaseModel):
    """Schema for user data used in rule evaluation"""
    age: int
    department: str
    salary: int
    experience: int

class RulesToCombine(BaseModel):
    """Schema for combining multiple rules"""
    rules: List[Dict[str, Any]]

class RuleEvaluation(BaseModel):
    """Schema for rule evaluation response"""
    result: bool
    evaluated_at: datetime = datetime.now()
    rules_evaluated: int

class RuleCombinationResponse(BaseModel):
    """Schema for combined rules response"""
    combined_rule: str
    rules_combined: int
    created_at: datetime = datetime.now()