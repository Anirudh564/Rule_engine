from flask import Blueprint, request, jsonify
from core.rule_engine import RuleEngine
from flask_login import login_required

api = Blueprint('api', __name__)
engine = RuleEngine()






@api.route('/modify_rule/<rule_id>', methods=['POST'])
@login_required
def modify_rule(rule_id):
    try:
        data = request.get_json()
        new_rule_string = data.get('rule')
        if not new_rule_string:
            return jsonify({'error': 'No rule provided'}), 400
        
        engine.modify_rule(rule_id, new_rule_string)  # Modify rule by id
        return jsonify({'message': 'Rule modified successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/delete_rule/<rule_id>', methods=['DELETE'])
@login_required
def delete_rule(rule_id):
    try:
        engine.delete_rule(rule_id)  # Implement this in your rule engine
        return jsonify({'message': 'Rule deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@api.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()
        rule_string = data.get('rule')
        if not rule_string:
            return jsonify({'error': 'No rule provided'}), 400
            
        rule_ast = engine.create_rule(rule_string)
        return jsonify({
            'message': 'Rule created successfully',
            'ast': rule_ast.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/combine_rules', methods=['POST'])
def combine_rules():
    try:
        data = request.get_json()
        rules = data.get('rules', [])
        if not rules:
            return jsonify({'error': 'No rules provided'}), 400
            
        combined_ast = engine.combine_rules(rules)
        return jsonify({
            'message': 'Rules combined successfully',
            'ast': combined_ast.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        data = request.get_json()
        rule_ast = data.get('rule')
        user_data = data.get('data')
        
        if not rule_ast or not user_data:
            return jsonify({'error': 'Missing rule or data'}), 400
            
        result = engine.evaluate_rule(rule_ast, user_data)
        return jsonify({
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400