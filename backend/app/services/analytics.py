from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

from app.schemas.analytics import StudentFeatures, AtRiskPrediction, AnalyticsRequest, AnalyticsResponse


class AtRiskPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
    
    def _prepare_features(self, students: List[StudentFeatures]) -> pd.DataFrame:
        """Convert student features to DataFrame for ML processing"""
        data = []
        for student in students:
            row = {
                'student_id': student.student_id,
                'gpa': student.gpa,
                'attendance_rate': student.attendance_rate,
                'credit_hours': student.credit_hours,
                'failed_courses': student.failed_courses,
                'age': student.age or 20,  # Default age if not provided
                'gender_encoded': 1 if student.gender == 'male' else 0 if student.gender == 'female' else 0.5
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def _generate_synthetic_training_data(self, n_samples: int = 1000) -> tuple:
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
        
        # Generate features
        gpa = np.random.normal(2.8, 0.8, n_samples)
        gpa = np.clip(gpa, 0, 4.0)
        
        attendance_rate = np.random.beta(8, 2, n_samples)  # Skewed towards higher attendance
        attendance_rate = np.clip(attendance_rate, 0, 1.0)
        
        credit_hours = np.random.normal(15, 3, n_samples)
        credit_hours = np.clip(credit_hours, 0, 30).astype(int)
        
        failed_courses = np.random.poisson(0.5, n_samples)
        failed_courses = np.clip(failed_courses, 0, 10)
        
        age = np.random.normal(22, 3, n_samples)
        age = np.clip(age, 18, 30).astype(int)
        
        gender = np.random.choice([0, 1], n_samples)
        
        # Create risk labels based on rules
        risk_labels = []
        for i in range(n_samples):
            risk_score = 0
            if gpa[i] < 2.0:
                risk_score += 3
            elif gpa[i] < 2.5:
                risk_score += 2
            elif gpa[i] < 3.0:
                risk_score += 1
            
            if attendance_rate[i] < 0.6:
                risk_score += 2
            elif attendance_rate[i] < 0.8:
                risk_score += 1
            
            if failed_courses[i] > 2:
                risk_score += 2
            elif failed_courses[i] > 0:
                risk_score += 1
            
            if credit_hours[i] < 12:
                risk_score += 1
            
            # Convert to binary classification
            risk_labels.append(1 if risk_score >= 3 else 0)
        
        features = pd.DataFrame({
            'gpa': gpa,
            'attendance_rate': attendance_rate,
            'credit_hours': credit_hours,
            'failed_courses': failed_courses,
            'age': age,
            'gender_encoded': gender
        })
        
        return features, np.array(risk_labels)
    
    def train(self):
        """Train the model with synthetic data"""
        X, y = self._generate_synthetic_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Store feature importance
        feature_names = ['gpa', 'attendance_rate', 'credit_hours', 'failed_courses', 'age', 'gender_encoded']
        self.feature_importance = dict(zip(feature_names, self.model.feature_importances_))
        
        self.is_trained = True
        
        return {
            'accuracy': accuracy,
            'feature_importance': self.feature_importance,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict(self, students: List[StudentFeatures]) -> List[AtRiskPrediction]:
        """Predict at-risk status for students"""
        if not self.is_trained:
            self.train()
        
        # Prepare features
        df = self._prepare_features(students)
        feature_cols = ['gpa', 'attendance_rate', 'credit_hours', 'failed_courses', 'age', 'gender_encoded']
        X = df[feature_cols].values
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get predictions and probabilities
        risk_probs = self.model.predict_proba(X_scaled)[:, 1]  # Probability of being at-risk
        risk_predictions = self.model.predict(X_scaled)
        
        predictions = []
        for i, student in enumerate(students):
            risk_score = float(risk_probs[i])
            risk_level = "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"
            confidence = float(max(risk_probs[i], 1 - risk_probs[i]))
            
            # Identify contributing factors
            factors = []
            if student.gpa < 2.5:
                factors.append("low_gpa")
            if student.attendance_rate < 0.8:
                factors.append("poor_attendance")
            if student.failed_courses > 1:
                factors.append("multiple_failures")
            if student.credit_hours < 12:
                factors.append("low_credit_load")
            
            predictions.append(AtRiskPrediction(
                student_id=student.student_id,
                risk_score=risk_score,
                risk_level=risk_level,
                confidence=confidence,
                factors=factors
            ))
        
        return predictions


def analyze_at_risk_students(request: AnalyticsRequest) -> AnalyticsResponse:
    """Main function to analyze at-risk students"""
    predictor = AtRiskPredictor()
    
    # Train model if not already trained
    if not predictor.is_trained:
        training_info = predictor.train()
    else:
        training_info = {"status": "model_already_trained"}
    
    # Make predictions
    predictions = predictor.predict(request.students)
    
    return AnalyticsResponse(
        predictions=predictions,
        model_info={
            "version": request.model_version,
            "algorithm": "RandomForest",
            "training_info": training_info,
            "feature_importance": predictor.feature_importance
        },
        generated_at=datetime.now()
    )
