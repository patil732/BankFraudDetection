# Exploratory Data Analysis (EDA) for Bank Transactions Fraud Detection

## 1. Dataset Overview

The dataset consists of bank transaction records with the following structure:

- **Size**: 2,512 transactions with 16 features
- **Target Variable**: `isFraud` (binary: 0 for legitimate, 1 for fraudulent)
- **Class Distribution**: Highly imbalanced (89 fraud vs 2,423 non-fraud cases)

### Features Categories:
- **Transaction Information**: TransactionID, Amount, Date, Type, Location, Channel
- **Customer Information**: Age, Occupation, Account Balance
- **Behavioral Information**: Transaction Duration, Login Attempts
- **Technical Information**: DeviceID, IP Address, MerchantID

## 2. Goals of EDA

- Understand the **distribution of fraud classes**
- Identify **key characteristics** of fraudulent transactions
- Analyze **relationships between numerical features** and fraud
- Examine **outliers and anomalies** in transaction patterns
- Detect and address **data quality issues**
- Guide **feature engineering and selection** strategies

## 3. Summary of Findings

### 3.1 Class Distribution
- **Severe class imbalance**: Only 3.54% of transactions are labeled as fraudulent
- **Implication**: Requires special handling techniques (SMOTE, class weights, etc.)

### 3.2 Key Correlations
| Feature Pair | Correlation | Interpretation |
|--------------|-------------|----------------|
| LoginAttempts & isFraud | 0.76 | Very strong relationship |
| TransactionAmount & isFraud | 0.22 | Moderate relationship |
| CustomerAge & AccountBalance | 0.32 | Moderate relationship |

### 3.3 Feature Distributions

| Feature | Distribution Pattern | Characteristics |
|---------|----------------------|----------------|
| TransactionAmount | Right-skewed | Many small transactions, few large ones |
| CustomerAge | Bimodal | Two predominant age groups |
| LoginAttempts | Heavily right-skewed | Mostly 1 attempt |
| TransactionDuration | Approximately normal | Centered distribution |
| AccountBalance | Right-skewed | Most accounts have moderate balances |

### 3.4 Outlier Detection

| Feature | Outlier Pattern | Implication |
|---------|-----------------|-------------|
| TransactionAmount | High-end outliers | Large transactions may need special attention |
| LoginAttempts | Many outliers (>1) | Multiple login attempts could indicate suspicious activity |
| AccountBalance | High-end outliers | Wealthy customers or potential money laundering |
| TransactionDuration | Both ends outliers | Unusually fast or slow transactions |
| CustomerAge | Few outliers | Generally consistent age distribution |

### 3.5 Data Quality Issues

1. **DateTime columns stored as objects** - Need conversion to datetime format
2. **Categorical variables need encoding** - For modeling compatibility
3. **Numerical features may benefit from scaling** - For algorithm performance

## 4. Next Steps

### 4.1 Data Preprocessing
- Convert DateTime columns to proper format
- Encode categorical variables (Location, TransactionType, Channel, etc.)
- Scale numerical features

### 4.2 Address Class Imbalance
- Apply techniques like SMOTE or ADASYN
- Use class weights in algorithms
- Consider anomaly detection approaches

### 4.3 Feature Engineering
- Create time-based features from transaction dates
- Engineer new features from existing ones
- Consider dimensionality reduction for high-cardinality categoricals

### 4.4 Model Selection
- Try tree-based models (Random Forest, XGBoost)
- Consider isolation forests for anomaly detection
- Evaluate neural networks for pattern recognition

### 4.5 Evaluation Metrics
- Focus on precision and recall rather than accuracy
- Use F1-score, AUC-ROC, and precision-recall curves
- Implement appropriate cross-validation strategies

## 5. Visualizations Summary

The EDA included several visualizations:

1. **Fraud distribution bar chart** - Showing class imbalance
2. **Correlation heatmap** - Revealing relationships between features
3. **Feature distribution histograms** - Showing data patterns for each numerical feature
4. **Boxplots** - Identifying outliers in each numerical feature

