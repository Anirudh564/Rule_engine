from typing import Dict, Any, Optional
import re

class RuleValidator:
    def __init__(self):
        self.valid_operators = {'AND', 'OR'}
        self.valid_comparisons = {'>', '<', '>=', '<=', '=', '!='}
        self.valid_attributes = {'age', 'department', 'salary', 'experience'}  # Add more as needed

    def validate_rule_string(self, rule_string: str) -> tuple[bool, Optional[str]]:
        """
        Validates the syntax of a rule string.
        Returns (is_valid, error_message)
        """
        if not rule_string:
            return False, "Rule string cannot be empty"

        # Check balanced parentheses
        if not self._check_balanced_parentheses(rule_string):
            return False, "Unbalanced parentheses in rule"

        # Remove whitespace for easier processing
        rule_string = ' '.join(rule_string.split())

        # Check for valid operators
        operators_found = re.findall(r'\b(AND|OR)\b', rule_string)
        if not all(op in self.valid_operators for op in operators_found):
            return False, "Invalid logical operator found"

        # Check conditions format
        conditions = re.findall(r'([a-zA-Z_]+)\s*([><=!]+)\s*([^AND|OR|)]+)', rule_string)
        for attribute, operator, value in conditions:
            # Check attribute
            if attribute.strip() not in self.valid_attributes:
                return False, f"Invalid attribute: {attribute}"

            # Check operator
            if operator.strip() not in self.valid_comparisons:
                return False, f"Invalid comparison operator: {operator}"

            # Check value format
            value = value.strip()
            if not self._validate_value_format(value):
                return False, f"Invalid value format: {value}"

        return True, None

    def validate_data(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validates the input data structure.
        Returns (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return False, "Data must be a dictionary"

        # Check for required attributes
        missing_attrs = self.valid_attributes - set(data.keys())
        if missing_attrs:
            return False, f"Missing required attributes: {missing_attrs}"

        # Validate data types
        for attr, value in data.items():
            if attr not in self.valid_attributes:
                return False, f"Invalid attribute: {attr}"

            if attr == 'age' or attr == 'experience':
                if not isinstance(value, (int, float)):
                    return False, f"{attr} must be a number"
            elif attr == 'salary':
                if not isinstance(value, (int, float)):
                    return False, f"salary must be a number"
            elif attr == 'department':
                if not isinstance(value, str):
                    return False, f"department must be a string"

        return True, None

    def _check_balanced_parentheses(self, rule_string: str) -> bool:
        """Check if parentheses are properly balanced in the rule string."""
        stack = []
        for char in rule_string:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return len(stack) == 0

    def _validate_value_format(self, value: str) -> bool:
        """Validate the format of a value in a condition."""
        value = value.strip().strip("'\"")
        
        # Check if it's a number
        try:
            float(value)
            return True
        except ValueError:
            # If not a number, it should be a valid string
            return bool(re.match(r'^[a-zA-Z0-9_\s-]+$', value))

    def validate_combined_rules(self, rules: list) -> tuple[bool, Optional[str]]:
        """
        Validates a list of rules for combination.
        Returns (is_valid, error_message)
        """
        if not rules:
            return False, "No rules provided"

        if not isinstance(rules, list):
            return False, "Rules must be provided as a list"

        for rule in rules:
            is_valid, error = self.validate_rule_string(rule)
            if not is_valid:
                return False, f"Invalid rule: {error}"

        return True, None