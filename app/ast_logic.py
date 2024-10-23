from typing import List, Dict, Any
import ast
import operator


class Node:
    def __init__(self, type: str, value: Any = None, left: 'Node' = None, right: 'Node' = None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

# Operator mapping
ops = {
    ast.And: operator.and_,
    ast.Or: operator.or_,
    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.Eq: operator.eq,
}

def create_rule(rule_string: str) -> Node:
    def build_ast(node):
        if isinstance(node, ast.BoolOp):
            return Node(
                type="operator",
                value=node.op.__class__,
                left=build_ast(node.values[0]),
                right=build_ast(node.values[1])
            )
        elif isinstance(node, ast.Compare):
            return Node(
                type="comparison",
                value=node.ops[0].__class__,
                left=build_ast(node.left),
                right=build_ast(node.comparators[0])
            )
        elif isinstance(node, ast.Name):
            return Node("variable", node.id)
        elif isinstance(node, ast.Num):
            return Node("constant", node.n)
        elif isinstance(node, ast.Str):
            return Node("constant", node.s)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    parsed = ast.parse(rule_string, mode='eval')
    return build_ast(parsed.body)

def combine_rules(rules: List[str]) -> Node:
    if not rules:
        raise ValueError("No rules to combine")
    if len(rules) == 1:
        return create_rule(rules[0])
    
    combined = create_rule(rules[0])
    for rule in rules[1:]:
        combined = Node(
            type="operator",
            value=ast.And,
            left=combined,
            right=create_rule(rule)
        )
    return combined

def evaluate_rule(root: Node, data: Dict[str, Any]) -> bool:
    if root.type == "operator":
        return ops[root.value](
            evaluate_rule(root.left, data),
            evaluate_rule(root.right, data)
        )
    elif root.type == "comparison":
        left_val = evaluate_rule(root.left, data)
        right_val = evaluate_rule(root.right, data)
        return ops[root.value](left_val, right_val)
    elif root.type == "variable":
        return data[root.value]
    elif root.type == "constant":
        return root.value
    else:
        raise ValueError(f"Unknown node type: {root.type}")

def node_to_string(node: Node) -> str:
    if node.type == "operator":
        op_str = "and" if node.value == ast.And else "or"
        return f"({node_to_string(node.left)} {op_str} {node_to_string(node.right)})"
    elif node.type == "comparison":
        op_str = {
            ast.Gt: ">",
            ast.Lt: "<",
            ast.GtE: ">=",
            ast.LtE: "<=",
            ast.Eq: "=="
        }[node.value]
        return f"({node_to_string(node.left)} {op_str} {node_to_string(node.right)})"
    elif node.type in ["variable", "constant"]:
        return str(node.value)
    else:
        raise ValueError(f"Unknown node type: {node.type}")