"""
Training script for Student Dropout Prediction Model
This script performs the same operations as the Jupyter notebook
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("Student Dropout Prediction Model Training")
print("=" * 60)

# Step 1: Load the dataset
print("\n[1/8] Loading dataset...")
df = pd.read_csv('dataset.csv')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {len(df.columns)}")

# Step 2: Check for missing values
print("\n[2/8] Checking for missing values...")
print(f"Missing values:\n{df.isnull().sum().sum()}")
print(f"\nTarget distribution:")
print(df['Target'].value_counts())

# Step 3: Feature Engineering
print("\n[3/8] Performing feature engineering...")
# Calculate attendance percentage
df['Attendance_1st_sem'] = df['Curricular units 1st sem (approved)'] / df['Curricular units 1st sem (enrolled)'].replace(0, 1) * 100
df['Attendance_2nd_sem'] = df['Curricular units 2nd sem (approved)'] / df['Curricular units 2nd sem (enrolled)'].replace(0, 1) * 100
df['Overall_Attendance'] = (df['Attendance_1st_sem'] + df['Attendance_2nd_sem']) / 2
df['Overall_Attendance'] = df['Overall_Attendance'].fillna(0)

# Calculate backlog (failed courses)
df['Backlog_1st_sem'] = df['Curricular units 1st sem (enrolled)'] - df['Curricular units 1st sem (approved)']
df['Backlog_2nd_sem'] = df['Curricular units 2nd sem (enrolled)'] - df['Curricular units 2nd sem (approved)']
df['Total_Backlog'] = df['Backlog_1st_sem'] + df['Backlog_2nd_sem']

# Average grade
df['Avg_Grade_1st'] = df['Curricular units 1st sem (grade)'].fillna(0)
df['Avg_Grade_2nd'] = df['Curricular units 2nd sem (grade)'].fillna(0)
df['Overall_Grade'] = (df['Avg_Grade_1st'] + df['Avg_Grade_2nd']) / 2
df['Overall_Grade'] = df['Overall_Grade'].fillna(0)

# Total enrolled courses
df['Total_Enrolled'] = df['Curricular units 1st sem (enrolled)'] + df['Curricular units 2nd sem (enrolled)']
print("Feature engineering completed!")

# Step 4: Select relevant features
print("\n[4/8] Selecting features...")
features = [
    'Age at enrollment',
    'Course',  # Degree
    'Tuition fees up to date',  # Fees status
    'Debtor',  # Family income indicator
    'Scholarship holder',
    'Gender',
    'Previous qualification',
    'Overall_Attendance',
    'Total_Backlog',
    'Overall_Grade',
    'Total_Enrolled',
    'Daytime/evening attendance',
    'Displaced',
    'Educational special needs',
    'International',
    'Curricular units 1st sem (enrolled)',
    'Curricular units 2nd sem (enrolled)'
]

X = df[features].copy()
y = df['Target'].copy()
print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Step 5: Encode target variable
print("\n[5/8] Encoding target variable...")
y_binary = (y == 'Dropout').astype(int)
print(f"Dropout rate: {y_binary.mean() * 100:.2f}%")
print(f"Target distribution:\n{y_binary.value_counts()}")

# Step 6: Split the data
print("\n[6/8] Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42, stratify=y_binary)
print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Step 7: Train Random Forest Classifier
print("\n[7/8] Training Random Forest Classifier...")
print("This may take a few minutes...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
print("Model trained successfully!")

# Step 8: Evaluate the model
print("\n[8/8] Evaluating model...")
y_pred = rf_model.predict(X_test)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]  # Probability of dropout

accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'='*60}")
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"{'='*60}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance
print("\nTop 10 Most Important Features:")
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance.head(10))

# Save the model and feature list
print("\nSaving model...")
joblib.dump(rf_model, 'dropout_model.pkl')
joblib.dump(features, 'model_features.pkl')
print("[OK] Model saved as 'dropout_model.pkl'")
print("[OK] Features saved as 'model_features.pkl'")

# Test prediction example
print("\n" + "="*60)
print("Testing with a sample prediction...")
sample_data = X_test.iloc[0:1]
prediction = rf_model.predict_proba(sample_data)[0][1] * 100
print(f"Sample dropout probability: {prediction:.2f}%")
print("="*60)

print("\n[OK] Training completed successfully!")
print("\nYou can now run the Flask application with: python app.py")

