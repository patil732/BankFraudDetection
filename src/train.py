import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_utils import DataProcessor
from model_training import ModelTrainer
from evaluate_model import ModelEvaluator


def main():
    print("=" * 60)
    print("FRAUD DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Initialize components
    data_processor = DataProcessor(random_state=42)
    model_trainer = ModelTrainer(random_state=42)
    
    # ------------------ FIXED DATA PATH ------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    data_path = os.path.join(PROJECT_ROOT, 'data', 'user_transaction_dataset.csv')
    # -----------------------------------------------------
    
    # Load data
    if not os.path.exists(data_path):
        print(f"❌ Data file not found at {data_path}")
        return False
    
    df = data_processor.load_data(data_path)
    
    # Validate target column
    if 'Is_Fraudulent' not in df.columns:
        print("❌ 'Is_Fraudulent' column not found in dataset")
        print("Available columns:", list(df.columns))
        return False
    
    # ---------------- FEATURE ENGINEERING ----------------
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    df = data_processor.feature_engineering(df)
    
    # Feature analysis
    categorical_cols, numerical_cols = data_processor.analyze_features(df)
    
    # ---------------- DATA PREPARATION ----------------
    print("\n" + "=" * 60)
    print("DATA PREPARATION")
    print("=" * 60)
    X_train, X_val, X_test, y_train, y_val, y_test = data_processor.prepare_data(df)
    
    # ---------------- MODEL TRAINING ----------------
    print("\n" + "=" * 60)
    print("MODEL TRAINING")
    print("=" * 60)
    
    preprocessor = model_trainer.create_preprocessor(
        categorical_cols,
        numerical_cols
    )
    
    detector = model_trainer.train(
        X_train,
        y_train,
        X_val,
        y_val
    )
    
    # ---------------- SAVE MODEL ----------------
    print("\n" + "=" * 60)
    print("SAVING MODEL")
    print("=" * 60)
    model_trainer.save_model()
    
    # ---------------- FINAL EVALUATION ----------------
    print("\n" + "=" * 60)
    print("FINAL EVALUATION")
    print("=" * 60)
    
    X_test_processed = preprocessor.transform(X_test)
    metrics, cm, report = detector.evaluate_model(
        X_test_processed,
        y_test
    )
    
    evaluator = ModelEvaluator()
    
    # Confusion Matrix
    evaluator.plot_confusion_matrix(
        cm,
        save_path=os.path.join(BASE_DIR, 'plots', 'confusion_matrix.png')
    )
    
    # Feature Importance (SAFE CHECK)
    if (
        hasattr(detector, "feature_importance")
        and detector.feature_importance is not None
    ):
        feature_names = model_trainer.get_feature_names()
        evaluator.plot_feature_importance(
            detector.feature_importance,
            feature_names,
            save_path=os.path.join(BASE_DIR, 'plots', 'feature_importance.png')
        )
    else:
        print("ℹ️ Feature importance not available for this model.")
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("📁 Model & preprocessor saved in: backend/models/")
    print("📊 Evaluation plots saved in: backend/plots/")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Training completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Training failed.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
