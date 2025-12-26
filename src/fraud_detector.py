import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import warnings
warnings.filterwarnings('ignore')

class FraudDetector:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.best_model = None
        self.feature_importance = None
        
    def create_models(self):
        """Create multiple models with regularization to prevent overfitting"""
        
        # XGBoost with strong regularization
        xgb_params = {
            'n_estimators': 200,
            'max_depth': 4,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 1.0,
            'reg_lambda': 1.0,
            # ❌ REMOVED scale_pos_weight (SMOTE already handles imbalance)
            'random_state': self.random_state,
            'n_jobs': -1,
            'verbosity': 0,
            'eval_metric': 'auc'   # ✅ ADDED (safe & recommended)
        }
        
        # Random Forest
        rf_params = {
            'n_estimators': 150,
            'max_depth': 8,
            'min_samples_split': 10,
            'min_samples_leaf': 5,
            'max_features': 'sqrt',
            'class_weight': 'balanced',
            'random_state': self.random_state,
            'n_jobs': -1,
            'bootstrap': True,
            'oob_score': True
        }
        
        # Logistic Regression
        lr_params = {
            'C': 0.1,
            'penalty': 'l2',
            'solver': 'liblinear',
            'class_weight': 'balanced',
            'random_state': self.random_state,
            'max_iter': 1000
        }
        
        # Gradient Boosting
        gb_params = {
            'n_estimators': 150,
            'learning_rate': 0.05,
            'max_depth': 3,
            'min_samples_split': 20,
            'min_samples_leaf': 10,
            'subsample': 0.8,
            'random_state': self.random_state
        }
        
        self.models = {
            'XGBoost': XGBClassifier(**xgb_params),
            'RandomForest': RandomForestClassifier(**rf_params),
            'LogisticRegression': LogisticRegression(**lr_params),
            'GradientBoosting': GradientBoostingClassifier(**gb_params)
        }
        
        return self.models
    
    def cross_validate_models(self, X, y, cv_folds=5):
        """Perform cross-validation"""
        cv_scores = {}
        
        for name, model in self.models.items():
            pipeline = ImbPipeline([
                ('smote', SMOTE(random_state=self.random_state)),
                ('classifier', model)
            ])
            
            cv = StratifiedKFold(
                n_splits=cv_folds,
                shuffle=True,
                random_state=self.random_state
            )
            
            scores = cross_val_score(
                pipeline,
                X,
                y,
                cv=cv,
                scoring='roc_auc',
                n_jobs=-1
            )
            
            cv_scores[name] = {
                'mean_auc': scores.mean(),
                'std_auc': scores.std(),
                'all_scores': scores
            }
            
            print(f"{name}: AUC = {scores.mean():.4f} (+/- {scores.std():.4f})")
        
        return cv_scores
    
    def select_best_model(self, cv_scores, X_train, y_train, X_val, y_val):
        """Select best model based on validation AUC"""
        best_score = -1
        best_model_name = None
        
        for name, model in self.models.items():
            pipeline = ImbPipeline([
                ('smote', SMOTE(random_state=self.random_state)),
                ('classifier', model)
            ])
            
            pipeline.fit(X_train, y_train)
            y_pred_prob = pipeline.predict_proba(X_val)[:, 1]
            val_auc = roc_auc_score(y_val, y_pred_prob)
            
            print(f"{name} Validation AUC: {val_auc:.4f}")
            
            if val_auc > best_score:
                best_score = val_auc
                best_model_name = name
                self.best_model = pipeline
        
        print(f"\nSelected model: {best_model_name} with AUC: {best_score:.4f}")
        
        # ✅ SAFE feature importance extraction
        clf = self.best_model.named_steps['classifier']
        if hasattr(clf, 'feature_importances_'):
            self.feature_importance = clf.feature_importances_
        
        return best_model_name, best_score
    
    def evaluate_model(self, X_test, y_test):
        """Comprehensive evaluation"""
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        y_pred = self.best_model.predict(X_test)
        y_pred_prob = self.best_model.predict_proba(X_test)[:, 1]
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_prob)
        }
        
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        print("\nTest Set Performance:")
        for k, v in metrics.items():
            print(f"{k.upper()}: {v:.4f}")
        
        return metrics, cm, report
