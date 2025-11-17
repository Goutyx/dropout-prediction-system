# Student Dropout Prediction System

A machine learning web application that predicts the dropout probability of students based on their academic and personal information. The system uses a Random Forest Classifier to analyze various student attributes and provides a percentage-based dropout risk assessment.

## Features

- **Machine Learning Model**: Random Forest Classifier trained on student dropout dataset
- **Web Interface**: Beautiful, responsive HTML/CSS/JavaScript frontend
- **RESTful API**: Flask backend for predictions
- **Real-time Predictions**: Get instant dropout probability percentages
- **Risk Assessment**: Categorizes students into Low, Medium, or High risk categories
- **Recommendations**: Provides actionable recommendations based on risk level

## Project Structure

```
archive/
├── dataset.csv                          # Student dropout dataset
├── student_dropout_prediction.ipynb    # Jupyter notebook for model training
├── app.py                              # Flask backend application
├── requirements.txt                    # Python dependencies
├── dropout_model.pkl                   # Trained model (generated after training)
├── model_features.pkl                  # Feature list (generated after training)
└── static/
    ├── style.css                       # Frontend styles
    └── script.js                       # Frontend JavaScript
    └── index.html                      # Frontend Front-end
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Jupyter Notebook (for model training)

## Installation & Setup

### Step 1: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- pandas (data manipulation)
- numpy (numerical computing)
- scikit-learn (machine learning)
- joblib (model serialization)

### Step 2: Train the Machine Learning Model

1. Open Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Open `student_dropout_prediction.ipynb`

3. Run all cells in the notebook (Cell → Run All)
   - This will:
     - Load and preprocess the dataset
     - Perform feature engineering
     - Train the Random Forest model
     - Evaluate the model performance
     - Save the trained model as `dropout_model.pkl` and `model_features.pkl`

4. Wait for the training to complete (this may take a few minutes)

### Step 3: Run the Flask Application

After the model is trained, start the Flask server:

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 4: Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Fill in the Student Information Form**:
   - Age at Enrollment
   - Course/Degree
   - Gender
   - Previous Qualification
   - Attendance Percentage
   - Backlog (failed courses)
   - Overall Grade
   - Tuition Fees Status
   - Family Income Indicators
   - And other relevant fields

2. **Click "Predict Dropout Probability"**

3. **View Results**:
   - Dropout probability percentage
   - Risk level (Low/Medium/High)
   - Recommendations

## Input Fields Explained

- **Age at Enrollment**: Student's age when enrolling
- **Course/Degree**: The academic program the student is enrolled in
- **Attendance (%)**: Percentage of courses successfully completed
- **Backlog**: Number of failed courses
- **Overall Grade**: Average grade across all courses (0-20 scale)
- **Tuition Fees Status**: Whether fees are up to date
- **Debtor**: Indicates family financial status
- **Scholarship Holder**: Whether student has a scholarship
- **Previous Qualification**: Educational background before enrollment

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 17 key features including age, course, attendance, grades, financial status, etc.
- **Output**: Dropout probability percentage (0-100%)
- **Risk Categories**:
  - **Low Risk**: < 30% dropout probability
  - **Medium Risk**: 30-60% dropout probability
  - **High Risk**: > 60% dropout probability

## API Endpoints

### POST /predict
Predicts dropout probability based on student data.

**Request Body** (JSON):
```json
{
  "age": 20,
  "course": 1,
  "fees_up_to_date": 1,
  "debtor": 0,
  "scholarship": 0,
  "gender": 1,
  "previous_qualification": 1,
  "attendance": 80.0,
  "backlog": 0,
  "overall_grade": 12.0,
  "total_enrolled": 12,
  "daytime_attendance": 1,
  "displaced": 1,
  "special_needs": 0,
  "international": 0,
  "enrolled_1st_sem": 6,
  "enrolled_2nd_sem": 6
}
```

**Response** (JSON):
```json
{
  "dropout_chance": 25.45,
  "risk_level": "Low",
  "recommendation": "Student is at low risk. Continue current support."
}
```

### GET /health
Health check endpoint to verify the server and model status.

## Troubleshooting

### Model Not Found Error
- Make sure you've run the Jupyter notebook to train and save the model
- Check that `dropout_model.pkl` and `model_features.pkl` exist in the project directory

### Port Already in Use
- If port 5000 is already in use, modify `app.py` to use a different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Dependencies Issues
- Make sure you're using Python 3.8 or higher
- Try upgrading pip: `python -m pip install --upgrade pip`
- Install dependencies individually if needed

## Future Enhancements

- Add data visualization for model insights
- Implement model retraining pipeline
- Add batch prediction capability
- Export prediction history
- Add authentication and user management
- Deploy to cloud platform

## License

This project is for educational purposes.

## Author

Student Dropout Prediction System - Machine Learning Project

## Acknowledgments

- Dataset: Student dropout dataset
- Libraries: scikit-learn, Flask, pandas, numpy

