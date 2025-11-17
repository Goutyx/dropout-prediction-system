function getValueOrDefault(id, defaultValue) {
    const element = document.getElementById(id);
    return element ? (element.value || defaultValue) : defaultValue;
}

document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    document.getElementById('loading').style.display = 'block';
    
    const formData = {
        age: parseInt(getValueOrDefault('age', 20)),
        course: parseInt(getValueOrDefault('course', 1)),
        fees_up_to_date: parseInt(getValueOrDefault('fees_up_to_date', 1)),
        debtor: parseInt(getValueOrDefault('debtor', 0)),
        scholarship: parseInt(getValueOrDefault('scholarship', 0)),
        gender: parseInt(getValueOrDefault('gender', 1)),
        previous_qualification: parseInt(getValueOrDefault('previous_qualification', 1)),
        attendance: parseFloat(getValueOrDefault('attendance', 80)),
        backlog: parseFloat(getValueOrDefault('backlog', 0)),
        overall_grade: parseFloat(getValueOrDefault('overall_grade', 12)),
        total_enrolled: parseInt(getValueOrDefault('total_enrolled', 12)),
        daytime_attendance: parseInt(getValueOrDefault('daytime_attendance', 1)),
        displaced: parseInt(getValueOrDefault('displaced', 1)),
        special_needs: parseInt(getValueOrDefault('health', 0)),
        international: parseInt(getValueOrDefault('international', 0)),
        enrolled_1st_sem: parseInt(getValueOrDefault('enrolled_1st_sem', 6)),
        enrolled_2nd_sem: parseInt(getValueOrDefault('enrolled_2nd_sem', 6))
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        document.getElementById('loading').style.display = 'none';
        
        if (response.ok) {
            showSpinnerAndResults(data);
        } else {
            showError(data.error || 'An error occurred while making the prediction.');
        }
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        showError('Network error: Could not connect to the server. Please make sure the Flask server is running.');
    }
});

function showSpinnerAndResults(data) {
    const resultDiv = document.getElementById('result');
    const spinnerContainer = document.getElementById('spinnerContainer');
    const percentageDisplay = document.getElementById('percentageDisplay');
    const resultDetails = document.getElementById('resultDetails');
    const dropoutPercentage = document.getElementById('dropoutPercentage');
    const percentageUnit = percentageDisplay.querySelector('.percentage-unit');
    const riskLevel = document.getElementById('riskLevel');
    const recommendation = document.getElementById('recommendation');
    
    resultDiv.style.display = 'block';
    spinnerContainer.style.display = 'flex';
    percentageDisplay.style.display = 'none';
    resultDetails.style.display = 'none';
    
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    setTimeout(() => {
        const dropoutChance = data.dropout_chance;
        
        spinnerContainer.style.display = 'none';
        
        percentageDisplay.style.display = 'flex';
        
        dropoutPercentage.textContent = dropoutChance.toFixed(2);
        
        if (dropoutChance >= 75) {
            dropoutPercentage.className = 'percentage-value red';
            percentageUnit.className = 'percentage-unit red';
        } else {
            dropoutPercentage.className = 'percentage-value green';
            percentageUnit.className = 'percentage-unit green';
        }
        
        setTimeout(() => {
            resultDetails.style.display = 'block';
            riskLevel.textContent = `Risk Level: ${data.risk_level}`;
            riskLevel.className = `risk-level ${data.risk_level.toLowerCase()}`;
            recommendation.textContent = data.recommendation;
        }, 500);
        
    }, 3000);
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'none';
    
    document.getElementById('spinnerContainer').style.display = 'none';
    document.getElementById('percentageDisplay').style.display = 'none';
    document.getElementById('resultDetails').style.display = 'none';
    
    const ageField = document.getElementById('age');
    if (ageField) ageField.value = 20;
    const attendanceField = document.getElementById('attendance');
    if (attendanceField) attendanceField.value = 80;
    const backlogField = document.getElementById('backlog');
    if (backlogField) backlogField.value = 0;
    const gradeField = document.getElementById('overall_grade');
    if (gradeField) gradeField.value = 12;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

