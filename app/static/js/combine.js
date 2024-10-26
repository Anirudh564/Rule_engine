document.addEventListener('DOMContentLoaded', function() {
    const combineForm = document.getElementById('combine-form');
    const rulesContainer = document.getElementById('rules-container');
    const addRuleButton = document.getElementById('add-rule');
    const operatorSelect = document.getElementById('operator-select');
    const resultDiv = document.getElementById('result');
    const astVisualization = document.getElementById('ast-visualization');

    addRuleButton.addEventListener('click', function() {
        const ruleEntry = document.createElement('div');
        ruleEntry.className = 'rule-entry';
        ruleEntry.innerHTML = `
            <input type="text" class="rule-input" placeholder="Enter rule...">
            <button type="button" class="btn btn-danger remove-rule">Remove</button>
        `;
        rulesContainer.appendChild(ruleEntry);

        // Add remove functionality
        ruleEntry.querySelector('.remove-rule').addEventListener('click', function() {
            ruleEntry.remove();
        });
    });

    combineForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const ruleInputs = document.querySelectorAll('.rule-input');
        const rules = Array.from(ruleInputs)
            .map(input => input.value.trim())
            .filter(rule => rule.length > 0);

        if (rules.length < 2) {
            showError('Please enter at least two rules to combine');
            return;
        }

        try {
            const response = await fetch('/api/combine_rules', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rules: rules,
                    operator: operatorSelect.value
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to combine rules');
            }

            showSuccess('Rules combined successfully!');
            visualizeAST(data.ast);
            
            // Store the combined AST for later use
            localStorage.setItem('lastCreatedRule', JSON.stringify(data.ast));

        } catch (error) {
            showError(error.message);
        }
    });

    function showError(message) {
        resultDiv.innerHTML = `<div class="error">${message}</div>`;
    }

    function showSuccess(message) {
        resultDiv.innerHTML = `<div class="success">${message}</div>`;
    }

    function visualizeAST(ast) {
        // Create a tree visualization of the combined AST
        astVisualization.innerHTML = '';
        
        function createNodeElement(node) {
            if (!node) return '';
            
            const nodeDiv = document.createElement('div');
            nodeDiv.className = `ast-node ${node.type}`;
            
            const valueDiv = document.createElement('div');
            valueDiv.className = 'node-value';
            valueDiv.textContent = node.value || '';
            nodeDiv.appendChild(valueDiv);
            
            if (node.left || node.right) {
                const childrenDiv = document.createElement('div');
                childrenDiv.className = 'node-children';
                
                if (node.left) {
                    childrenDiv.appendChild(createNodeElement(node.left));
                }
                if (node.right) {
                    childrenDiv.appendChild(createNodeElement(node.right));
                }
                
                nodeDiv.appendChild(childrenDiv);
            }
            
            return nodeDiv;
        }
        
        astVisualization.appendChild(createNodeElement(ast));
    }

    // Add initial example rules
    const exampleRules = [
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
        "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
    ];

    exampleRules.forEach((rule, index) => {
        if (index === 0) {
            rulesContainer.querySelector('.rule-input').value = rule;
        } else {
            const ruleEntry = document.createElement('div');
            ruleEntry.className = 'rule-entry';
            ruleEntry.innerHTML = `
                <input type="text" class="rule-input" value="${rule}">
                <button type="button" class="btn btn-danger remove-rule">Remove</button>
            `;
            rulesContainer.appendChild(ruleEntry);

            ruleEntry.querySelector('.remove-rule').addEventListener('click', function() {
                ruleEntry.remove();
            });
        }
    });
});