Rule Engine with AST
Overview
This repository contains a simple 3-tier rule engine application designed to evaluate user eligibility based on dynamic rules. The rule engine uses an Abstract Syntax Tree (AST) to represent conditional rules and allows for the creation, combination, and modification of these rules.

The system includes:

A user-friendly front-end to create, view, and evaluate rules.
An API that handles rule creation and evaluation.
A backend that processes the rules and evaluates user attributes like age, department, income, etc.
Features
Dynamic Rule Creation: Create complex rules using a simple UI.
Rule Combination: Combine multiple rules into one logical expression.
Rule Evaluation: Evaluate rules against user attributes such as age, department, salary, etc.
Login Required: Secured endpoints requiring users to log in.
Error Handling: Graceful error handling for invalid rules or missing data.
Project Structure
bash
Copy code
RULE_ENGINE/
│
├── app/
│   ├── routes/                # Backend routing
│   ├── static/                # Static files (CSS, JS)
│   ├── templates/             # HTML templates
│   └── __init__.py            # Initialize the app
│
├── core/
│   ├── rule_engine.py         # Main rule engine logic
│   ├── user.py                # User-related logic
│   ├── validators.py          # Validators for rule engine
│
├── tests/
│   ├── test_rule_engine.py    # Unit tests for the rule engine
│   ├── test_api.py            # API tests
│
├── config/                    # Configurations for the app
│   ├── development.py
│   ├── production.py
│
├── venv/                      # Python virtual environment
│
├── run.py                     # Entry point for running the app
├── requirements.txt           # List of dependencies
├── README.md                  # Project documentation (this file)
└── .gitignore                 # Ignored files in version control
Getting Started
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7 or higher
A virtual environment tool (like venv or virtualenv)
Flask (for running the web server)
Setup Instructions
Clone the Repository:

bash
Copy code
git clone https://github.com/your_username/rule-engine-ast.git
cd rule-engine-ast
Set Up Virtual Environment: Create a virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies: Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Database Setup (if using a database): Configure your database in config/development.py or config/production.py. For SQLite, you can simply run the following command to initialize the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Application: Start the Flask app:

bash
Copy code
python run.py
Access the Application: Open a browser and go to:

arduino
Copy code
http://127.0.0.1:5000/
Running Tests
To run the tests, you can use the pytest tool:

bash
Copy code
pytest tests/
Usage
Create Rules: Use the UI to create dynamic rules using a string-based format (e.g., age > 30 AND department = 'Sales').
View Rules: Navigate to the "View Rules" page to see all created rules.
Evaluate Rules: Evaluate the rules based on the user's input data (e.g., {"age": 35, "department": "Sales", "salary": 60000}).
Sample API Endpoints
POST /create_rule: Create a new rule.
POST /combine_rules: Combine multiple rules into one.
POST /evaluate_rule: Evaluate a rule against given data.
Example Rule
Here is an example of a rule string:

java
Copy code
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
Contributing
Contributions are welcome! If you would like to improve this project, feel free to:

Fork the repository.
Create a new branch (git checkout -b feature/new-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/new-feature).
Open a pull request.
