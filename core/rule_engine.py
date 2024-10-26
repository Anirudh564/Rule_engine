from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import re

@dataclass
class Node:
    type: str  # "operator" or "operand"
    value: Optional[str] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

class RuleEngine:
    def __init__(self):
        self.operators = {'AND', 'OR'}
        self.comparisons = {'>', '<', '>=', '<=', '=', '!='}

    def tokenize(self, rule_string: str) -> List[str]:
        # Replace parentheses with spaces around them
        rule_string = re.sub(r'([()])', r' \1 ', rule_string)
        # Ensure spaces around comparison operators
        for op in self.comparisons:
            rule_string = rule_string.replace(op, f' {op} ')
        return [token for token in rule_string.split() if token.strip()]

    def parse_condition(self, tokens: List[str], pos: int) -> tuple[Node, int]:
        attribute = tokens[pos]
        operator = tokens[pos + 1]
        value = tokens[pos + 2]
        
        # Create leaf node for the condition
        node = Node(
            type="operand",
            value=f"{attribute} {operator} {value}"
        )
        return node, pos + 3

    def parse_expression(self, tokens: List[str], pos: int = 0) -> tuple[Node, int]:
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")

        if tokens[pos] == '(':
            left_node, pos = self.parse_expression(tokens, pos + 1)
        else:
            left_node, pos = self.parse_condition(tokens, pos)

        if pos >= len(tokens) or tokens[pos] == ')':
            return left_node, pos + 1

        if tokens[pos] not in self.operators:
            raise ValueError(f"Expected operator, got {tokens[pos]}")

        operator = tokens[pos]
        right_node, pos = self.parse_expression(tokens, pos + 1)

        return Node(type="operator", value=operator, left=left_node, right=right_node), pos

    def create_rule(self, rule_string: str) -> Node:
        tokens = self.tokenize(rule_string)
        ast, _ = self.parse_expression(tokens)
        return ast
    def get_all_rules(self):
        return [{"id": rule_id, "rule_string": str(rule)} for rule_id, rule in self.rules.items()]

    def modify_rule(self, rule_id, new_rule_string):
        if rule_id not in self.rules:
            raise Exception("Rule not found")
        self.rules[rule_id] = self.parse_rule(new_rule_string)

    def delete_rule(self, rule_id):
        if rule_id in self.rules:
            del self.rules[rule_id]
        else:
            raise Exception("Rule not found")
        
        
    def combine_rules(self, rules: List[str], operator: str = "AND") -> Node:
        if not rules:
            raise ValueError("No rules provided")
        if len(rules) == 1:
            return self.create_rule(rules[0])

        # Create ASTs for all rules
        rule_asts = [self.create_rule(rule) for rule in rules]
        
        # Combine ASTs using the specified operator
        combined = rule_asts[0]
        for ast in rule_asts[1:]:
            combined = Node(
                type="operator",
                value=operator,
                left=combined,
                right=ast
            )
        
        return combined

    def evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        # Parse condition string (e.g., "age > 30")
        parts = condition.split()
        attribute, operator, value = parts[0], parts[1], ' '.join(parts[2:])
        
        # Get actual value from data
        if attribute not in data:
            raise ValueError(f"Attribute {attribute} not found in data")
        
        actual_value = data[attribute]
        
        # Convert value to appropriate type
        try:
            if isinstance(actual_value, (int, float)):
                value = float(value.strip("'\""))
            else:
                value = value.strip("'\"")
        except ValueError:
            raise ValueError(f"Invalid value type for comparison: {value}")

        # Evaluate condition
        if operator == '>':
            return actual_value > value
        elif operator == '<':
            return actual_value < value
        elif operator == '>=':
            return actual_value >= value
        elif operator == '<=':
            return actual_value <= value
        elif operator == '=':
            return actual_value == value
        elif operator == '!=':
            return actual_value != value
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def evaluate_rule(self, ast: Dict[str, Any], data: Dict[str, Any]) -> bool:
        # Convert dict back to Node if necessary
        if isinstance(ast, dict):
            node = Node(
                type=ast['type'],
                value=ast['value'],
                left=ast['left'] if ast['left'] else None,
                right=ast['right'] if ast['right'] else None
            )
        else:
            node = ast

        if node.type == "operand":
            return self.evaluate_condition(node.value, data)
        
        left_result = self.evaluate_rule(node.left, data)
        right_result = self.evaluate_rule(node.right, data)
        
        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {node.value}")