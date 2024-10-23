from tortoise import fields, models


# Tortoise ORM Models
class RuleModel(models.Model):
    """Database model for storing rules"""
    id = fields.IntField(pk=True)
    rule_string = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
    last_modified = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "rules"

    def __str__(self):
        return f"Rule {self.id}: {self.rule_string}"

    class PydanticMeta:
        exclude = ["created_at", "last_modified"]