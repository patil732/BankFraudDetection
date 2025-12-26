from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from model_persistence import ModelManager

app = Flask(__name__)
CORS(app)

# Initialize model manager
model_manager = ModelManager()
models_loaded = False

def load_models_on_startup():
    """Attempt to load models when the API starts"""
    global models_loaded
    try:
        models_loaded = model_manager.load_models()
    except Exception as e:
        print(f"Failed to load models on startup: {str(e)}")
        models_loaded = False

# Load models when app starts
load_models_on_startup()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'api_status': 'running',
        'model_loaded': models_loaded,
        'preprocessor_loaded': models_loaded
    }
    return jsonify(status), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if a transaction is fraudulent"""
    if not models_loaded:
        return jsonify({
            'error': 'Models not loaded. Please train the model first.',
            'instructions': 'Run: python train.py'
        }), 503
    
    try:
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame
        if isinstance(data, dict):
            # Single prediction
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            # Multiple predictions
            df = pd.DataFrame(data)
        else:
            return jsonify({'error': 'Invalid data format'}), 400
        
        # Make prediction
        predictions, probabilities = model_manager.predict(df)
        
        # Prepare response
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'transaction_id': i,
                'is_fraud': bool(pred),
                'fraud_probability': float(prob[1]),
                'legit_probability': float(prob[0]),
                'risk_level': 'HIGH' if prob[1] > 0.7 else 'MEDIUM' if prob[1] > 0.3 else 'LOW'
            })
        
        return jsonify({
            'predictions': results,
            'total_transactions': len(results),
            'fraud_count': int(sum(predictions))
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Predict for multiple transactions from a CSV file"""
    if not models_loaded:
        return jsonify({
            'error': 'Models not loaded. Please train the model first.'
        }), 503
    
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check file extension
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Make predictions
        predictions, probabilities = model_manager.predict(df)
        
        # Add predictions to dataframe
        df['is_fraud_predicted'] = predictions
        df['fraud_probability'] = probabilities[:, 1]
        df['legit_probability'] = probabilities[:, 0]
        
        # Convert to JSON
        results = df.to_dict('records')
        
        return jsonify({
            'results': results,
            'total_transactions': len(results),
            'fraud_count': int(sum(predictions)),
            'fraud_percentage': (sum(predictions) / len(predictions)) * 100
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reload_models', methods=['POST'])
def reload_models():
    """Reload models from disk"""
    global models_loaded
    try:
        models_loaded = model_manager.load_models()
        return jsonify({
            'success': True,
            'model_loaded': models_loaded,
            'message': 'Models reloaded successfully' if models_loaded else 'Failed to load models'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    
    print("=" * 60)
    print("FRAUD DETECTION API")
    print("=" * 60)
    print(f"Model loaded: {models_loaded}")
    print(f"Preprocessor loaded: {models_loaded}")
    
    if not models_loaded:
        print("\n⚠️  WARNING: Models not loaded!")
        print("To fix this:")
        print("1. Train the model: python train.py")
        print("2. Make sure these files exist:")
        print("   - models/trained_detector.pkl")
        print("   - models/preprocessor.pkl")
    
    print("\nAPI running on http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("-" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)