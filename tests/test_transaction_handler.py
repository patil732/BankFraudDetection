import os
import json
from src.transaction_handler import TransactionHandler


def test_process_and_log(tmp_path, monkeypatch):
    # Use a temp file for fraud attempts
    fh = TransactionHandler(initial_balance=1000, load_history=False)
    tx = {
        'amount Transaction': 100,
        'Merchant': 'Test',
        'location Transaction': 'City',
        'payment_channel': 'UPI'
    }

    success, msg = fh.process_transaction(tx, is_fraud=False)
    assert success is True
    assert fh.get_balance() == 900
