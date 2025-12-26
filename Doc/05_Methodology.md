# Methodology

## Technical Approach

This document outlines the technical methodology employed in the Intelligent Fraud Detection System.

---

## 1. Data Preprocessing Pipeline

### Data Cleaning
- Removal of duplicate records
- Handling missing values using appropriate imputation strategies
- Outlier detection and treatment
- Data type validation and conversion

### Feature Normalization
- Standard scaling for numerical features
- Categorical encoding using One-Hot Encoder
- Min-Max scaling for bounded features (probabilities, percentages)

---

## 2. Feature Engineering

### Temporal Features
- **Hour of Transaction**: Captures time-based fraud patterns
- **Day of Week**: Weekend vs. weekday spending differences
- **Month**: Seasonal spending variations
- **Day of Month**: End-of-month spike patterns
- **Time Since Last Transaction**: User frequency analysis

### Geographic Features
- **Location Encoding**: Merchant and customer locations
- **Location Consistency**: Flagging unusual geographic deviations
- **Distance from Home**: Travel-based anomalies

### Behavioral Features
- **Transaction Frequency**: Average transactions per user per day
- **Average Spending Amount**: User-specific baseline
- **Spending Category Distribution**: Preferred merchant categories
- **Transaction Velocity**: Rapid successive transactions
- **New Merchant Flag**: First-time interactions with merchants

### Statistical Features
- **Z-Score Normalization**: Deviation from user average
- **Rolling Statistics**: 7-day and 30-day moving averages
- **Coefficient of Variation**: Spending variability index

---

## 3. Machine Learning Models

### Supervised Learning Models

#### Random Forest Classifier
- **Purpose**: Ensemble method for robust classification
- **Advantages**: Handles non-linear relationships, provides feature importance
- **Hyperparameters**: 100 trees, max_depth=15, min_samples_split=10
- **Use Case**: Detecting known fraud patterns from historical data

#### XGBoost Classifier
- **Purpose**: Gradient boosting for superior predictive performance
- **Advantages**: Feature importance ranking, fast inference, handles imbalance
- **Hyperparameters**: learning_rate=0.1, max_depth=6, n_estimators=100
- **Use Case**: Primary model for fraud classification

### Unsupervised Learning Models

#### Isolation Forest
- **Purpose**: Anomaly detection without labeled examples
- **Advantages**: Efficient for high-dimensional data, no distance computation
- **Hyperparameters**: contamination=0.05, random_state=42
- **Use Case**: Detecting novel fraud patterns not in training data

#### One-Class SVM
- **Purpose**: Outlier detection based on support vectors
- **Advantages**: Robust to skewed distributions, non-linear boundary detection
- **Hyperparameters**: nu=0.05, kernel='rbf', gamma='scale'
- **Use Case**: User behavior deviation detection

---

## 4. Class Imbalance Handling

### Problem
- Real-world fraud datasets have ~99% legitimate and ~1% fraudulent transactions
- Standard models tend to ignore minority class
- Simple accuracy metric becomes misleading

### Solutions Implemented

#### SMOTE (Synthetic Minority Over-sampling Technique)
- Creates synthetic fraud samples in feature space
- Applied to training data only (prevents data leakage)
- k_neighbors=5 for generating synthetic samples

#### Class Weighting
- Assigns higher weight to fraudulent class during training
- Formula: weight = total_samples / (n_classes * class_samples)
- Automatically handled by scikit-learn `class_weight='balanced'`

#### Stratified Sampling
- Maintains class distribution during train-test split
- Stratified K-Fold cross-validation for unbiased evaluation

---

## 5. Model Training Pipeline

### Data Splitting
```
Total Dataset → Train (70%) → Test (30%)
             → Train (70%) → Validation (20%), Training (50%)
```

### Cross-Validation Strategy
- **5-Fold Stratified Cross-Validation** for hyperparameter tuning
- **Hold-out test set** for final performance evaluation
- **Temporal validation**: Optional time-based splitting for time-series assessment

### Hyperparameter Tuning
- **Grid Search** for exhaustive parameter exploration
- **Validation metric**: F1-Score (balances precision and recall for imbalanced data)
- **Early Stopping**: For XGBoost to prevent overfitting

---

## 6. Ensemble Strategy

### Voting Classifier
- Combines predictions from Random Forest and XGBoost
- Hard voting for binary classification
- Soft voting using probability estimates for nuanced decisions

### Score Aggregation
```
Fraud Risk Score = (RF_prob + XGBoost_prob + Isolation_score + SVM_score) / 4
```

### Decision Rules
- **Score ≥ 0.7**: Flagged as High-Risk (Fraud)
- **0.4 ≤ Score < 0.7**: Medium-Risk (Requires Review)
- **Score < 0.4**: Low-Risk (Legitimate)

---

## 7. Risk Scoring Engine

### Components
1. **Model Predictions**: Aggregated probability from all models
2. **Anomaly Score**: Deviation from user baseline
3. **Velocity Score**: Rapid transaction frequency indicator
4. **Geographic Score**: Location-based risk assessment
5. **Behavioral Score**: Pattern deviation from user profile

### Risk Calculation
```
Final Risk Score = 0.4 * Model_Pred + 0.2 * Anomaly + 0.15 * Velocity 
                 + 0.15 * Geographic + 0.1 * Behavioral
```

---

## 8. Model Evaluation Metrics

### Classification Metrics
- **Accuracy**: Overall correctness
- **Precision**: True positives among predicted positives (reduces false alarms)
- **Recall**: True positives among actual positives (catches frauds)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under receiver operating characteristic curve
- **PR-AUC**: Precision-Recall curve for imbalanced data

### Confusion Matrix Analysis
```
                 Predicted Negative    Predicted Positive
Actual Negative        TN                    FP
Actual Positive        FN                    TP
```

---

## 9. Model Persistence

### Serialization
- Models saved using Joblib library
- Preprocessing pipeline (StandardScaler, OneHotEncoder) serialized together
- Metadata stored: model version, training date, performance metrics

### Directory Structure
```
src/models/
├── random_forest_model.pkl
├── xgboost_model.pkl
├── isolation_forest_model.pkl
├── svm_model.pkl
├── preprocessor.pkl
└── model_metadata.json
```

### Loading Strategy
- Lazy loading on API startup
- Validation of model integrity and compatibility
- Fallback mechanisms for missing or corrupted models

---

## 10. Real-Time Inference Pipeline

### Input Processing
1. Receive transaction data via API
2. Validate input format and data types
3. Feature engineering on new transaction
4. Data standardization using saved preprocessor

### Prediction
1. Load trained models
2. Generate predictions from all models
3. Aggregate predictions using ensemble method
4. Calculate final risk score

### Output Generation
1. Classification result (Fraud/Legitimate)
2. Risk score (0-1 probability)
3. Model confidence levels
4. Feature contributions (top influencing factors)
5. User alert notification (if fraudulent)

---

## 11. Continuous Improvement

### Model Monitoring
- Track prediction accuracy over time
- Monitor for data drift and distribution changes
- Compare actual vs. predicted outcomes

### Retraining Schedule
- Periodic retraining with new labeled data
- Performance degradation thresholds trigger retraining
- A/B testing for new model versions

### Feedback Loop
- User validation of fraud alerts
- False positive/negative analysis
- Incorporation of new fraud patterns into training data
