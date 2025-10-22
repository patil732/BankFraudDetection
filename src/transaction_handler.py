import pandas as pd
import datetime
import os
import json

class TransactionHandler:
    def __init__(self, initial_balance=10000, history_path='transaction_history.json', fraud_attempts_file='fraud_attempts.txt', load_history=True):
        """Transaction handler.

        Args:
            initial_balance: starting balance
            history_path: path to transaction history JSON
            fraud_attempts_file: path to append fraud logs
            load_history: if True, load existing history from history_path
        """
        self.balance = initial_balance
        self.transaction_history = []
        self.history_path = history_path
        self.fraud_attempts_file = fraud_attempts_file

        # Load existing transaction history if available (optional)
        if load_history:
            self._load_transaction_history()
        
    def _load_transaction_history(self):
        """Load transaction history from file if exists"""
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, 'r') as f:
                    data = json.load(f)
                    self.transaction_history = data.get('transactions', [])
                    self.balance = data.get('balance', self.balance)
                    print(f"Loaded {len(self.transaction_history)} transactions from history")
        except Exception as e:
            print(f"Error loading transaction history: {e}")
    
    def _save_transaction_history(self):
        """Save transaction history to file"""
        try:
            with open(self.history_path, 'w') as f:
                json.dump({
                    'transactions': self.transaction_history,
                    'balance': self.balance
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving transaction history: {e}")
    
    def process_transaction(self, transaction_data, is_fraud, user_approved=False):
        """Process a transaction based on fraud status and user approval"""
        transaction_id = f"TXN{len(self.transaction_history) + 10000}"
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        transaction_record = {
            'transaction_id': transaction_id,
            'timestamp': current_time,
            **transaction_data,
            'is_fraud_detected': is_fraud,
            'user_approved': user_approved,
            'status': 'pending'
        }
        
        try:
            if is_fraud and not user_approved:
                # Log fraud attempt and cancel transaction
                transaction_record['status'] = 'cancelled_fraud'
                self._log_fraud_attempt(transaction_record)
                self.transaction_history.append(transaction_record)
                self._save_transaction_history()
                return False, "Transaction cancelled due to suspected fraud."
            
            elif is_fraud and user_approved:
                # User overrode fraud detection - proceed with warning
                if self.balance >= transaction_data['amount Transaction']:
                    self.balance -= transaction_data['amount Transaction']
                    transaction_record['status'] = 'completed_override'
                    self.transaction_history.append(transaction_record)
                    self._save_transaction_history()
                    return True, "Transaction completed (user overrode fraud detection)."
                else:
                    transaction_record['status'] = 'failed_insufficient_funds'
                    self.transaction_history.append(transaction_record)
                    self._save_transaction_history()
                    return False, "Insufficient funds for this transaction."
            
            else:
                # Normal transaction
                if self.balance >= transaction_data['amount Transaction']:
                    self.balance -= transaction_data['amount Transaction']
                    transaction_record['status'] = 'completed'
                    self.transaction_history.append(transaction_record)
                    self._save_transaction_history()
                    return True, "Transaction completed successfully."
                else:
                    transaction_record['status'] = 'failed_insufficient_funds'
                    self.transaction_history.append(transaction_record)
                    self._save_transaction_history()
                    return False, "Insufficient funds for this transaction."
                    
        except Exception as e:
            transaction_record['status'] = 'failed_error'
            self.transaction_history.append(transaction_record)
            self._save_transaction_history()
            return False, f"Transaction failed: {str(e)}"
    
    def _log_fraud_attempt(self, transaction_record):
        """Log fraud attempts to a text file"""
        log_entry = f"""
Fraud Attempt Detected and Blocked:
Transaction ID: {transaction_record['transaction_id']}
Timestamp: {transaction_record['timestamp']}
Amount: ${transaction_record['amount Transaction']:.2f}
Merchant: {transaction_record['Merchant']}
Location: {transaction_record['location Transaction']}
Payment Channel: {transaction_record['payment_channel']}
---
"""
        
        try:
            with open(self.fraud_attempts_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error logging fraud attempt: {e}")
    
    def get_transaction_history(self):
        """Get transaction history"""
        return self.transaction_history
    
    def get_balance(self):
        """Get current balance"""
        return self.balance