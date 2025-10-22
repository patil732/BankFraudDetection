from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime
import os
import random
import traceback

# Ensure Flask finds templates located in the src/templates directory
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Local model and handler imports (relative to src)
from fraud_model import FraudDetectionModel
from transaction_handler import TransactionHandler

# Initialize model and transaction handler
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'fraud_model.pkl')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')

fraud_model = FraudDetectionModel()
model_loaded = fraud_model.load_model(MODEL_PATH, SCALER_PATH)

transaction_handler = TransactionHandler()

# Mock data - we'll use this until the model is properly loaded
mock_transactions = [
    {
        'id': 1,
        'amount': 45.50,
        'merchant': 'Amazon',
        'location': 'Seattle, WA', 
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'completed',
        'fraud_probability': 12
    },
    {
        'id': 2, 
        'amount': 23.75,
        'merchant': 'Starbucks',
        'location': 'New York, NY',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'completed',
        'fraud_probability': 5
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "message": "API is running"
    })

@app.route('/api/balance')
def get_balance():
    return jsonify({
        "name": "John Doe",
        "account": "•••• 4832", 
        "balance": 10000.00,
        "currency": "$"
    })

@app.route('/api/transactions')
def get_transactions():
    try:
        return jsonify(mock_transactions)
    except Exception as e:
        print(f"Error getting transactions: {e}")
        return jsonify([])

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "total_transactions": len(mock_transactions),
        "fraud_detected": 0,
        "approved_transactions": len(mock_transactions),
        "blocked_transactions": 0
    })

@app.route('/api/transaction/predict', methods=['POST'])
def predict_transaction():
    try:
        data = request.json
        # Build transaction payload expected by the model
        amount = float(data.get('amount', 0))
        transaction_data = {
            'amount Transaction': amount,
            'Merchant': data.get('merchant', 'Unknown'),
            'merchant_category': data.get('merchant_category', 'Unknown'),
            'location Transaction': data.get('location', 'Unknown'),
            'payment_channel': data.get('payment_channel', 'Unknown'),
            'device_used': data.get('device_used', 'Unknown'),
            'date Transaction': data.get('date Transaction', datetime.datetime.now().strftime("%d-%m-%Y")),
            'time Transaction': data.get('time Transaction', datetime.datetime.now().strftime("%H:%M:%S"))
        }

        reasons = []
        fraud_probability = 0
        is_fraud = False

        # If the trained model is available, use it; otherwise fall back to simple rules
        if model_loaded:
            try:
                pred, prob = fraud_model.predict_fraud(transaction_data)
                is_fraud = bool(pred)
                fraud_probability = round(float(prob) * 100, 2)
            except Exception as e:
                print(f"Model prediction failed: {e}")
                traceback.print_exc()
                model_err = True
        else:
            # Fallback rule-based scoring (simple risk rules)
            merchant = data.get('merchant', '').lower()
            location = data.get('location', '').lower()
            if amount <= 0:
                fraud_probability += 40
                reasons.append("Unusual transaction amount")
            elif amount > 1000:
                fraud_probability += 25
            if merchant == 'unknown':
                fraud_probability += 30
                reasons.append("Suspicious merchant pattern")
            if location == 'unknown':
                fraud_probability += 20
                reasons.append("Unverified location")
            # Random variance
            fraud_probability += random.randint(-10, 20)
            fraud_probability = max(5, min(95, fraud_probability))
            is_fraud = fraud_probability > 50
        
        return jsonify({
            "is_fraud": is_fraud,
            "fraud_probability": fraud_probability,
            "transaction_data": transaction_data,
            "flagged_reasons": reasons
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            "is_fraud": False,
            "fraud_probability": 10,
            "transaction_data": {},
            "flagged_reasons": []
        })

@app.route('/api/transaction/process', methods=['POST'])
def process_transaction():
    try:
        data = request.json
        # Expect { transaction_data: {...}, fraud_probability: n, user_approved: bool (optional) }
        tx = data.get('transaction_data', {})
        fraud_probability = data.get('fraud_probability', 0)
        user_approved = data.get('user_approved', False)

        # Use transaction handler to process
        success, message = transaction_handler.process_transaction(tx, is_fraud=bool(fraud_probability > 50), user_approved=user_approved)

        # Return updated balance and status
        return jsonify({
            "success": success,
            "message": message,
            "new_balance": transaction_handler.get_balance(),
            "transaction_history": transaction_handler.get_transaction_history()
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Transaction failed: {str(e)}"
        })

if __name__ == '__main__':
    print("Starting Bank Fraud Detection API...")
    print("Using mock data for testing")
    print("API running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)