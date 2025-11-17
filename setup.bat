@echo off
echo ========================================
echo Student Dropout Prediction System Setup
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setup complete!
echo.
echo Next steps:
echo 1. Open Jupyter Notebook: jupyter notebook
echo 2. Run student_dropout_prediction.ipynb to train the model
echo 3. After training, run: python app.py
echo 4. Open browser to: http://localhost:5000
echo.
pause

