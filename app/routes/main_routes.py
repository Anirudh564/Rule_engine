from flask_login import login_required
from flask import Blueprint, render_template
from core.rule_engine import RuleEngine


main = Blueprint('main', __name__)
engine = RuleEngine()



@main.route('/')
def index():
    return render_template('index.html')



@main.route('/create')
def create():
    return render_template('create.html')

@main.route('/combine')
def combine():
    return render_template('combine.html')

@main.route('/evaluate')
def evaluate():
    return render_template('evaluate.html')