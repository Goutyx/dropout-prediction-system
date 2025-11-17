from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

try:
    model = joblib.load('dropout_model.pkl')
    model_features = joblib.load('model_features.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    model_features = None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict dropout probability"""
    try:
        if model is None or model_features is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        age = float(data.get('age', 20))
        course = int(data.get('course', 1))
        fees_up_to_date = int(data.get('fees_up_to_date', 1))
        debtor = int(data.get('debtor', 0))
        scholarship = int(data.get('scholarship', 0))
        gender = int(data.get('gender', 1))
        previous_qualification = int(data.get('previous_qualification', 1))
        attendance = float(data.get('attendance', 80))
        backlog = float(data.get('backlog', 0))
        overall_grade = float(data.get('overall_grade', 12))
        total_enrolled = int(data.get('total_enrolled', 12))
        daytime_attendance = int(data.get('daytime_attendance', 1))
        displaced = int(data.get('displaced', 1))
        special_needs = int(data.get('special_needs', 0))
        international = int(data.get('international', 0))
        enrolled_1st_sem = int(data.get('enrolled_1st_sem', 6))
        enrolled_2nd_sem = int(data.get('enrolled_2nd_sem', 6))
        
        features_array = np.array([[
            age,
            course,
            fees_up_to_date,
            debtor,
            scholarship,
            gender,
            previous_qualification,
            attendance,
            backlog,
            overall_grade,
            total_enrolled,
            daytime_attendance,
            displaced,
            special_needs,
            international,
            enrolled_1st_sem,
            enrolled_2nd_sem
        ]])
        
        dropout_probability = model.predict_proba(features_array)[0][1] * 100
        
        dropout_chance = round(dropout_probability, 2)
        
        if dropout_chance < 30:
            risk_level = "Low"
            recommendation = "Student is at low risk. Continue current support."
        elif dropout_chance < 60:
            risk_level = "Medium"
            recommendation = "Student needs attention. Provide additional support and counseling."
        else:
            risk_level = "High"
            recommendation = "Student is at high risk. Immediate intervention required."
        
        return jsonify({
            'dropout_chance': dropout_chance,
            'risk_level': risk_level,
            'recommendation': recommendation
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    if not os.path.exists('dropout_model.pkl'):
        print("Warning: dropout_model.pkl not found. Please run the Jupyter notebook first to train the model.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

