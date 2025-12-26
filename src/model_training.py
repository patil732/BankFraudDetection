from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

class ModelTrainer:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.preprocessor = None
        self.model = None
        
    def create_preprocessor(self, categorical_cols, numerical_cols):
        """Create preprocessing pipeline"""
        self.categorical_cols = categorical_cols
        self.numerical_cols = numerical_cols

        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )
        
        return self.preprocessor
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        from fraud_detector import FraudDetector
        
        detector = FraudDetector(random_state=self.random_state)
        detector.create_models()
        
        print("Preprocessing data...")
        X_train_processed = self.preprocessor.fit_transform(X_train)
        X_val_processed = None
        
        if X_val is not None:
            X_val_processed = self.preprocessor.transform(X_val)
        
        feature_names = self.get_feature_names()
        print(f"Number of features after preprocessing: {len(feature_names)}")
        
        print("\nCross-validation results:")
        cv_scores = detector.cross_validate_models(X_train_processed, y_train)
        
        if X_val is not None:
            print("\nValidation set performance:")
            detector.select_best_model(
                cv_scores,
                X_train_processed,
                y_train,
                X_val_processed,
                y_val
            )
        
        self.model = detector.best_model
        
        if X_val is not None:
            self.check_overfitting(X_train_processed, y_train, X_val_processed, y_val)
        
        return detector
    
    def get_feature_names(self):
        """Correct feature name extraction"""
        if self.preprocessor is None:
            return []

        feature_names = []

        # Numeric features (names stay same)
        feature_names.extend(self.numerical_cols)

        # Categorical feature names from OneHotEncoder
        ohe = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
        cat_feature_names = ohe.get_feature_names_out(self.categorical_cols)
        feature_names.extend(cat_feature_names)

        return feature_names
    
    def check_overfitting(self, X_train, y_train, X_val, y_val):
        from sklearn.metrics import roc_auc_score
        
        y_train_pred_prob = self.model.predict_proba(X_train)[:, 1]
        train_auc = roc_auc_score(y_train, y_train_pred_prob)
        
        y_val_pred_prob = self.model.predict_proba(X_val)[:, 1]
        val_auc = roc_auc_score(y_val, y_val_pred_prob)
        
        auc_diff = train_auc - val_auc
        
        print(f"\nOverfitting Check:")
        print(f"Training AUC: {train_auc:.4f}")
        print(f"Validation AUC: {val_auc:.4f}")
        print(f"Difference: {auc_diff:.4f}")
        
        if auc_diff > 0.1:
            print("⚠️ WARNING: Potential overfitting detected!")
        elif auc_diff > 0.05:
            print("⚠️ Moderate overfitting detected")
        else:
            print("✅ Good generalization")
    
    def save_model(self, model_path='models/trained_detector.pkl',
                  preprocessor_path='models/preprocessor.pkl'):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")
        
        joblib.dump(self.preprocessor, preprocessor_path)
        print(f"Preprocessor saved to {preprocessor_path}")
