import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class MLEngine:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize ML model with pre-trained weights or train on synthetic data"""
        # For hackathon demo, use rule-based + simple ML hybrid
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        
        # Generate synthetic training data for demo
        self._train_on_synthetic_data()
    
    def _train_on_synthetic_data(self):
        """Train model on synthetic patient data for demo purposes"""
        np.random.seed(42)
        
        # Generate 1000 synthetic patient records
        n_samples = 1000
        
        # Features: age, severity, chronic_illness, pregnancy_elderly, rural_indicator, travel_distance
        X = np.random.rand(n_samples, 6)
        
        # Age: 1-100
        X[:, 0] = np.random.randint(1, 101, n_samples)
        
        # Severity: 1-10
        X[:, 1] = np.random.randint(1, 11, n_samples)
        
        # Chronic illness: 0 or 1
        X[:, 2] = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
        
        # Pregnancy/elderly: 0 or 1
        X[:, 3] = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
        
        # Rural indicator: 0 or 1
        X[:, 4] = np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
        
        # Travel distance: 1-200 km
        X[:, 5] = np.random.uniform(1, 200, n_samples)
        
        # Generate target urgency scores based on logical rules
        y = self._generate_urgency_scores(X)
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def _generate_urgency_scores(self, X):
        """Generate realistic urgency scores based on patient features"""
        urgency_scores = np.zeros(len(X))
        
        for i, features in enumerate(X):
            age, severity, chronic, preg_elderly, rural, distance = features
            
            # Base urgency from severity
            urgency = severity * 10
            
            # Age factors
            if age < 5 or age > 70:
                urgency += 15
            elif age < 18 or age > 60:
                urgency += 10
            
            # Chronic illness adds urgency
            if chronic:
                urgency += 20
            
            # Pregnancy/elderly flag
            if preg_elderly:
                urgency += 25
            
            # Rural patients get priority boost
            if rural:
                urgency += 15
            
            # Distance factor (longer distance = higher urgency)
            if distance > 100:
                urgency += 20
            elif distance > 50:
                urgency += 10
            
            # Add some randomness
            urgency += np.random.normal(0, 5)
            
            # Normalize to 0-100 scale
            urgency_scores[i] = max(0, min(100, urgency))
        
        return urgency_scores
    
    def predict_urgency(self, patient_data):
        """Predict urgency score and priority level for a patient"""
        if not self.is_trained:
            self._initialize_model()
        
        # Extract features
        features = np.array([
            patient_data['age'],
            patient_data['symptom_severity'],
            1 if patient_data['chronic_illness'] else 0,
            1 if patient_data['pregnancy_elderly'] else 0,
            1 if patient_data['location'].lower() == 'rural' else 0,
            patient_data['travel_distance']
        ]).reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict urgency score
        urgency_score = self.model.predict(features_scaled)[0]
        
        # Determine priority level
        if urgency_score >= 70:
            priority_level = 'High'
        elif urgency_score >= 40:
            priority_level = 'Medium'
        else:
            priority_level = 'Low'
        
        return urgency_score, priority_level
    
    def get_feature_importance(self):
        """Get feature importance for model interpretation"""
        if self.model and self.is_trained:
            feature_names = ['Age', 'Severity', 'Chronic Illness', 'Pregnancy/Elderly', 'Rural', 'Distance']
            importance = self.model.feature_importances_
            return dict(zip(feature_names, importance))
        return {}