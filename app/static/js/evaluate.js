document.addEventListener('DOMContentLoaded', function() {
    const evaluateForm = document.getElementById('evaluate-form');
    const dataInput = document.getElementById('data-input');
    const storedRuleDisplay = document.getElementById('stored-rule');
    const loadRuleButton = document.getElementById('load-rule');
    const resultDiv = document.getElementById('result');

    let currentRule = null;

    loadRuleButton.addEventListener('click', function() {
        const storedRule = localStorage.getItem('lastCreatedRule');
        if (storedRule) {
            currentRule = JSON.parse(storedRule);
            storedRuleDisplay.textContent = JSON.stringify(currentRule, null, 2);
            storedRuleDisplay.classList.add('rule-loaded');
        } else {
            showError('No stored rule found. Please create a rule first.');
        }
    });

    evaluateForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (!currentRule) {
            showError('Please load a rule first');
            return;
        }

        let userData;
        try {
            userData = JSON.parse(dataInput.value);
        } catch (error) {
            showError('Invalid JSON format in user data');
            return;
        }

        try {
            const response = await fetch('/api/evaluate_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rule: currentRule,
                    data: userData
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to evaluate rule');
            }

            showResult(data.result);

        } catch (error) {
            showError(error.message);
        }
    });

    function showError(message) {
        resultDiv.className = 'result-panel result-failure';
        resultDiv.innerHTML = `<strong>Error:</strong> ${message}`;
    }

    function showResult(result) {
        resultDiv.className = 'result-panel ' + (result ? 'result-success' : 'result-failure');
        resultDiv.innerHTML = `
            <strong>Evaluation Result:</strong> 
            ${result ? 'User matches the rule criteria' : 'User does not match the rule criteria'}
        `;
    }

    // Initialize with sample data
    dataInput.value = JSON.stringify({
        age: 35,
        department: "Sales",
        salary: 60000,
        experience: 3
    }, null, 4);
});