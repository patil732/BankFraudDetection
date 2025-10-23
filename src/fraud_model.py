import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import warnings
warnings.filterwarnings('ignore')

# model fnHandler

class FraudDetectionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def clean_column_names(self, df):
        """Clean column names by stripping whitespace"""
        df = df.copy()
        df.columns = df.columns.str.strip()
        return df
        
    def preprocess_data(self, df):
        """Preprocess the transaction data for model training"""
        # Clean column names first
        data = self.clean_column_names(df)
        
        print("Columns found:", data.columns.tolist())
        
        # Convert date and time to datetime features
        data['datetime'] = pd.to_datetime(
            data['date Transaction'] + ' ' + data['time Transaction'], 
            format='%d-%m-%Y %H:%M:%S'
        )
        
        # Extract time-based features
        data['hour'] = data['datetime'].dt.hour
        data['day_of_week'] = data['datetime'].dt.dayofweek
        data['month'] = data['datetime'].dt.month
        data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
        data['is_night'] = ((data['hour'] >= 22) | (data['hour'] <= 6)).astype(int)
        
        # Feature engineering
        data['amount'] = data['amount Transaction']
        data['log_amount'] = np.log1p(data['amount'])
        
        # Categorical columns to encode
        categorical_cols = ['Merchant', 'merchant_category', 'location Transaction', 
                           'payment_channel', 'device_used']
        
        # Label encode categorical variables
        for col in categorical_cols:
            # Fill missing with explicit unknown marker
            data[col] = data[col].fillna('unknown').astype(str)
            if col not in self.label_encoders:
                le = LabelEncoder()
                # Fit encoder and ensure it knows about the 'unknown' token so prediction doesn't crash
                values_to_fit = list(data[col].unique())
                if 'unknown' not in values_to_fit:
                    values_to_fit.append('unknown')
                le.fit(values_to_fit)
                self.label_encoders[col] = le
                data[col] = le.transform(data[col])
            else:
                # If encoder already exists (e.g., when re-processing), map unseen to 'unknown' then transform
                le = self.label_encoders[col]
                known = set(le.classes_)
                data[col] = data[col].apply(lambda x: x if x in known else 'unknown')
                data[col] = le.transform(data[col])
        
        # Select features for model
        feature_columns = ['amount', 'log_amount', 'hour', 'day_of_week', 'month', 
                         'is_weekend', 'is_night'] + categorical_cols
        
        self.feature_columns = feature_columns
        
        # Use the cleaned column name for fraud label
        return data[feature_columns], data['Fraud label']
    
    def train_model(self, df):
        """Train the fraud detection model"""
        print("Preprocessing data...")
        X, y = self.preprocess_data(df)
        
        print(f"Training data shape: {X.shape}")
        print(f"Fraud cases: {y.sum()} out of {len(y)} transactions")
        
        print("Splitting data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        
        print("\nModel Evaluation:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Feature Importances:")
        print(feature_importance.head(10))
        
        return self.model
    
    def predict_fraud(self, transaction_data):
        """Predict if a transaction is fraudulent"""
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Convert to DataFrame
        transaction_df = pd.DataFrame([transaction_data])
        
        # Clean column names
        transaction_df = self.clean_column_names(transaction_df)
        
        # Preprocess the transaction
        try:
            # Create datetime
            transaction_df['datetime'] = pd.to_datetime(
                transaction_df['date Transaction'] + ' ' + transaction_df['time Transaction'], 
                format='%d-%m-%Y %H:%M:%S'
            )
            
            # Extract features
            transaction_df['hour'] = transaction_df['datetime'].dt.hour
            transaction_df['day_of_week'] = transaction_df['datetime'].dt.dayofweek
            transaction_df['month'] = transaction_df['datetime'].dt.month
            transaction_df['is_weekend'] = transaction_df['day_of_week'].isin([5, 6]).astype(int)
            transaction_df['is_night'] = ((transaction_df['hour'] >= 22) | (transaction_df['hour'] <= 6)).astype(int)
            transaction_df['amount'] = transaction_df['amount Transaction']
            transaction_df['log_amount'] = np.log1p(transaction_df['amount'])
            
            # Encode categorical variables safely (map unseen categories to 'unknown')
            for col in ['Merchant', 'merchant_category', 'location Transaction', 
                       'payment_channel', 'device_used']:
                if col in transaction_df.columns and col in self.label_encoders:
                    transaction_df[col] = transaction_df[col].fillna('unknown').astype(str)
                    le = self.label_encoders[col]
                    known = set(le.classes_)
                    transaction_df[col] = transaction_df[col].apply(lambda x: x if x in known else 'unknown')
                    transaction_df[col] = le.transform(transaction_df[col])
                else:
                    # If encoder not available, fill with 0 to avoid exceptions
                    if col in transaction_df.columns:
                        transaction_df[col] = 0
            
            # Select features
            X = transaction_df[self.feature_columns]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Predict
            prediction = self.model.predict(X_scaled)[0]
            probability = self.model.predict_proba(X_scaled)[0][1]
            
            return prediction, probability
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return 0, 0.0  # Default to non-fraudulent if error
    
    def save_model(self, model_path='models/fraud_model.pkl', scaler_path='models/scaler.pkl'):
        """Save the trained model and scaler"""
        import os
        os.makedirs('models', exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns
            }, f)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
    
    def load_model(self, model_path='models/fraud_model.pkl', scaler_path='models/scaler.pkl'):
        """Load the trained model and scaler"""
        try:
            with open(model_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.model = saved_data['model']
                self.label_encoders = saved_data['label_encoders']
                self.feature_columns = saved_data['feature_columns']
            
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            print("Model loaded successfully!")
            return True
        except FileNotFoundError:
            print("Model files not found. Please train the model first.")
            return False

# Train the model if this script is run directly
if __name__ == "__main__":
    try:
        # Load your data
        print("Loading data...")
        df = pd.read_csv('data/modified_Chaitanya_Student_Transactions_with_merchant_category.csv')
        
        print(f"Data loaded with {len(df)} transactions")
        print(f"Columns: {df.columns.tolist()}")
        
        # Clean column names for the main dataframe
        df.columns = df.columns.str.strip()
        
        # Initialize and train model
        fraud_model = FraudDetectionModel()
        fraud_model.train_model(df)
        
        # Save the model
        fraud_model.save_model()
        
        print("\nModel training completed successfully!")
        
    except Exception as e:
        print(f"Error during model training: {e}")
        import traceback
        traceback.print_exc()