document.addEventListener('DOMContentLoaded', function() {
    const ruleForm = document.getElementById('rule-form');
    const ruleInput = document.getElementById('rule-input');
    const resultDiv = document.getElementById('result');
    const visualizationDiv = document.getElementById('rule-visualization');

    ruleForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const rule = ruleInput.value.trim();
        if (!rule) {
            showError('Please enter a rule');
            return;
        }

        try {
            const response = await fetch('/api/create_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ rule })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to create rule');
            }

            showSuccess('Rule created successfully!');
            visualizeAST(data.ast);
            
            // Store the AST in localStorage for later use
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
        // Create a tree visualization of the AST
        visualizationDiv.innerHTML = '';
        const tree = document.createElement('div');
        tree.className = 'ast-tree';
        
        function createNode(node) {
            if (!node) return null;
            
            const nodeDiv = document.createElement('div');
            nodeDiv.className = `ast-node ${node.type}`;
            
            const valueDiv = document.createElement('div');
            valueDiv.className = 'node-value';
            valueDiv.textContent = node.value || '';
            nodeDiv.appendChild(valueDiv);
            
            const childrenDiv = document.createElement('div');
            childrenDiv.className = 'node-children';
            
            if (node.left) {
                childrenDiv.appendChild(createNode(node.left));
            }
            if (node.right) {
                childrenDiv.appendChild(createNode(node.right));
            }
            
            if (node.left || node.right) {
                nodeDiv.appendChild(childrenDiv);
            }
            
            return nodeDiv;
        }
        
        tree.appendChild(createNode(ast));
        visualizationDiv.appendChild(tree);
    }

    // Add example rules
    const exampleRules = [
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
        "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
    ];

    const examplesDiv = document.getElementById('rule-examples');
    if (examplesDiv) {
        examplesDiv.innerHTML = '<h3>Example Rules:</h3>' + exampleRules.map(rule => 
            `<div class="example-rule" onclick="document.getElementById('rule-input').value = this.innerText;">${rule}</div>`
        ).join('');
    }
});