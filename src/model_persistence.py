import joblib
import numpy as np
import pandas as pd
import os

class ModelManager:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        
    def load_models(self,
                    model_path='models/trained_detector.pkl',
                    preprocessor_path='models/preprocessor.pkl'):
        """Load trained model and preprocessor"""

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, model_path)
        preprocessor_path = os.path.join(BASE_DIR, preprocessor_path)

        try:
            self.model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"❌ Model file not found at {model_path}")
            return False
        
        try:
            self.preprocessor = joblib.load(preprocessor_path)
            print(f"✅ Preprocessor loaded from {preprocessor_path}")
        except FileNotFoundError:
            print(f"❌ Preprocessor file not found at {preprocessor_path}")
            return False
        
        return True
    
    def predict(self, data):
        """Make predictions on batch data"""
        if self.model is None or self.preprocessor is None:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        # Preprocess
        processed_data = self.preprocessor.transform(data)
        
        predictions = self.model.predict(processed_data)
        probabilities = self.model.predict_proba(processed_data)
        
        return predictions, probabilities
    
    def predict_single(self, transaction_data):
        """Predict for a single transaction"""
        if isinstance(transaction_data, dict):
            df = pd.DataFrame([transaction_data])
        elif isinstance(transaction_data, pd.DataFrame):
            df = transaction_data
        else:
            raise ValueError("transaction_data must be dict or DataFrame")
        
        predictions, probabilities = self.predict(df)
        
        return {
            'prediction': int(predictions[0]),
            'fraud_probability': float(probabilities[0][1]),
            'legit_probability': float(probabilities[0][0]),
            'is_fraud': bool(predictions[0])
        }
