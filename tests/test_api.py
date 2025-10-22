import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app


def test_health():
    client = app.test_client()
    rv = client.get('/api/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'status' in data


def test_predict_and_process():
    client = app.test_client()

    payload = {
        'amount': 12.5,
        'merchant': 'Starbucks',
        'location': 'Seattle'
    }

    rv = client.post('/api/transaction/predict', json=payload)
    assert rv.status_code == 200
    pred = rv.get_json()
    assert 'is_fraud' in pred

    # Process the predicted transaction
    process_payload = {
        'transaction_data': pred['transaction_data'],
        'fraud_probability': pred['fraud_probability'],
        'user_approved': False
    }

    rv2 = client.post('/api/transaction/process', json=process_payload)
    assert rv2.status_code == 200
    resp = rv2.get_json()
    assert 'success' in resp
