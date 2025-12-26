import numpy as np

class RiskScorer:
    def __init__(self):
        pass
        
    def calculate_risk_score(self, transaction, user_history=None):
        """Calculate comprehensive risk score"""
        risk_score = 0
        factors = []
        
        # -------- Amount-based risk --------
        amount = transaction.get('Transaction_Amount', 0)
        if amount > 10000:
            risk_score += 30
            factors.append('High amount (>10,000)')
        elif amount > 5000:
            risk_score += 20
            factors.append('Medium amount (>5,000)')
        
        # -------- Time-based risk --------
        hour = transaction.get('Hour', 12)
        if 0 <= hour <= 6:
            risk_score += 25
            factors.append('Night-time transaction')
        
        # -------- Location risk --------
        location = transaction.get('Location', '').lower()
        if location not in ['mumbai', 'pune', 'delhi', 'bangalore', 'chennai', 'hyderabad']:
            risk_score += 20
            factors.append('Unusual location')
        
        # -------- User history risk --------
        if user_history:
            avg_amount = user_history.get('avg_amount', 0)
            if avg_amount > 0 and amount > avg_amount * 3:
                risk_score += 40
                factors.append('Amount > 3x user average')
            
            freq = user_history.get('transaction_count', 1)
            if freq > 20:
                risk_score += 15
                factors.append('High frequency user')
        
        # -------- Device risk --------
        device = transaction.get('Device_Type', '').lower()
        if device in ['web browser', 'unknown']:
            risk_score += 10
            factors.append('Unusual device')
        
        # -------- Normalize --------
        risk_score = min(100, risk_score)
        
        # -------- Risk level --------
        if risk_score >= 70:
            risk_level = 'HIGH'
        elif risk_score >= 40:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': factors,
            'recommendation': self.get_recommendation(risk_score)
        }
    
    def get_recommendation(self, risk_score):
        if risk_score >= 70:
            return 'BLOCK - High risk transaction'
        elif risk_score >= 40:
            return 'REVIEW - Manual verification required'
        elif risk_score >= 20:
            return 'MONITOR - Additional checks recommended'
        else:
            return 'APPROVE - Low risk transaction'
