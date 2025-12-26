import pandas as pd
from datetime import datetime

class UserProfiler:
    def __init__(self):
        self.user_profiles = {}
    
    def create_user_profile(self, user_id, transactions_df):
        """Create behavioral profile for a user"""
        user_transactions = transactions_df[transactions_df['User_ID'] == user_id]
        
        if len(user_transactions) == 0:
            return None
        
        profile = {
            'user_id': user_id,
            'total_transactions': len(user_transactions),
            'avg_transaction_amount': user_transactions['Transaction_Amount'].mean(),
            'max_transaction_amount': user_transactions['Transaction_Amount'].max(),
            'common_merchant_categories': user_transactions['Merchant_Category'].mode().tolist()[:3],
            'common_transaction_channels': user_transactions['Transaction_Channel'].mode().tolist()[:3],
            'usual_hours': self._get_usual_hours(user_transactions),
            'usual_locations': user_transactions['Location'].mode().tolist()[:3],
            'fraud_rate': user_transactions['Is_Fraudulent'].mean(),
            'last_update': datetime.now().isoformat()
        }
        
        self.user_profiles[user_id] = profile
        return profile
    
    def _get_usual_hours(self, transactions):
        """Get usual transaction hours"""
        if 'Hour' in transactions.columns:
            hour_counts = transactions['Hour'].value_counts()
            usual_hours = hour_counts[hour_counts > len(transactions) * 0.1].index.tolist()
            return sorted(usual_hours)[:5]
        return []
    
    def detect_behavioral_anomalies(self, current_transaction, user_profile):
        """Detect anomalies vs user behavior"""
        anomalies = []
        
        # Amount anomaly
        avg_amount = user_profile['avg_transaction_amount']
        current_amount = float(current_transaction.get('Transaction_Amount', 0))
        
        if current_amount > avg_amount * 3:
            anomalies.append(
                f"Transaction amount ({current_amount}) is 3x higher than average ({avg_amount:.2f})"
            )
        
        # Time anomaly
        current_hour = int(current_transaction.get('Hour', 12))
        usual_hours = user_profile.get('usual_hours', [])
        if usual_hours and current_hour not in usual_hours:
            anomalies.append(f"Unusual transaction hour: {current_hour}")
        
        # Location anomaly
        current_location = current_transaction.get('Location', '')
        usual_locations = user_profile.get('usual_locations', [])
        if usual_locations and current_location not in usual_locations:
            anomalies.append(f"Unusual location: {current_location}")
        
        # Merchant category anomaly
        current_merchant = current_transaction.get('Merchant_Category', '')
        common_categories = user_profile.get('common_merchant_categories', [])
        if common_categories and current_merchant not in common_categories:
            anomalies.append(f"Unusual merchant category: {current_merchant}")
        
        return anomalies
    
    def update_profile(self, user_id, new_transaction):
        """Update user profile incrementally"""
        if user_id not in self.user_profiles:
            return False
        
        profile = self.user_profiles[user_id]
        new_amount = float(new_transaction.get('Transaction_Amount', 0))
        total_trans = profile['total_transactions']
        
        # Update average
        old_avg = profile['avg_transaction_amount']
        profile['avg_transaction_amount'] = (
            old_avg * total_trans + new_amount
        ) / (total_trans + 1)
        
        # Update max
        profile['max_transaction_amount'] = max(
            profile['max_transaction_amount'],
            new_amount
        )
        
        profile['total_transactions'] += 1
        profile['last_update'] = datetime.now().isoformat()
        
        return True
    
    def get_user_risk_profile(self, user_id):
        """Return risk summary for user"""
        if user_id not in self.user_profiles:
            return None
        
        profile = self.user_profiles[user_id]
        fraud_rate = profile['fraud_rate']
        
        if fraud_rate > 0.1:
            risk_level = 'High Risk User'
        elif fraud_rate > 0.05:
            risk_level = 'Medium Risk User'
        elif fraud_rate > 0.01:
            risk_level = 'Low Risk User'
        else:
            risk_level = 'Trusted User'
        
        return {
            'user_id': user_id,
            'risk_level': risk_level,
            'fraud_rate': fraud_rate,
            'total_transactions': profile['total_transactions'],
            'behavioral_consistency': self._calculate_consistency_score(profile),
            'profile_completeness': self._calculate_completeness_score(profile)
        }
    
    def _calculate_consistency_score(self, profile):
        if profile['total_transactions'] < 10:
            return 50
        elif profile['total_transactions'] > 50:
            return 90
        else:
            return 70
    
    def _calculate_completeness_score(self, profile):
        required_fields = [
            'avg_transaction_amount',
            'common_merchant_categories',
            'common_transaction_channels',
            'usual_hours'
        ]
        
        complete_fields = sum(
            1 for field in required_fields
            if profile.get(field)
        )
        
        return (complete_fields / len(required_fields)) * 100
