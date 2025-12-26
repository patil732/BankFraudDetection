# **Intelligent Fraud Detection in Financial Transactions**

## **Project Overview**

This project is an **Intelligent Fraud Detection System** that combines **supervised and unsupervised machine learning** to detect fraudulent financial transactions in real-time. The system analyzes transaction patterns, user behavior, and spending profiles to identify fraudulent activities while minimizing false positives.

It is built using **Flask**, **Machine Learning algorithms**, and **advanced feature engineering**, providing a comprehensive web-based interface for fraud analysis and prediction.

---

## **Features**

- Detects **fraudulent transactions** using multiple ML algorithms (Random Forest, XGBoost, Isolation Forest).
- Performs **real-time anomaly scoring** to identify unusual spending patterns.
- Builds **user-specific spending profiles** based on temporal, spatial, and behavioral features.
- Handles **class imbalance** using advanced techniques (SMOTE, class weighting).
- Provides **risk scoring** for transactions with detailed explanations.
- Displays **sentiment distribution and insights** through interactive visualizations.
- Offers a **user-friendly web interface** built with Flask for easy fraud investigation.
- Implements **supervised learning** for detecting known fraud types and **unsupervised learning** for anomaly detection.

---

## **System Architecture**

### **Core Components**

1. **Data Pipeline** - Data collection, cleaning, and preprocessing
2. **Feature Engineering** - Time-based, location-based, and behavioral features
3. **Model Training** - Supervised and unsupervised model development
4. **Risk Scoring Engine** - Real-time anomaly detection and risk calculation
5. **Web Application** - Flask-based API and interactive UI
6. **Model Persistence** - Joblib-based model serialization for production use

---

## **Phases of the Project**

### **1. Data Collection**
- Sourced financial transaction dataset with both legitimate and fraudulent records
- Dataset contains features: transaction amount, merchant category, time, location, and class labels
- Identified significant class imbalance (majority legitimate, minority fraudulent)

### **2. Data Preprocessing & Feature Engineering**
- Handling missing values and data normalization
- Extracting temporal features: hour, day, month, day of week
- Geographic feature extraction: transaction locations, velocity
- Behavioral features: spending categories, transaction frequency, average spending
- Statistical features: z-scores, rolling statistics for anomaly detection

### **3. Model Development**
- **Supervised Learning**: Random Forest and XGBoost classifiers for known fraud detection
- **Unsupervised Learning**: Isolation Forest and One-Class SVM for anomaly detection
- **Ensemble Methods**: Combined approach for robust predictions
- **Class Imbalance Handling**: SMOTE, class weighting, and stratified sampling

### **4. User Profile Modeling**
- Building dynamic user-specific spending profiles
- Creating baseline behavior patterns from transaction history
- Detecting deviations from normal user behavior

### **5. Real-Time Detection & Risk Scoring**
- Integrated anomaly scores with classifier predictions
- Multi-factor risk assessment combining multiple detection methods
- Automated alert generation for suspicious transactions
- Transaction validation and feedback mechanisms

### **6. Performance Evaluation & Optimization**
- Cross-validation and hyperparameter tuning
- Evaluation metrics: Precision, Recall, F1-Score, ROC-AUC
- Model comparison and selection
- Performance monitoring and optimization

### **7. Web Application Development**
- RESTful API endpoints for fraud prediction
- Real-time transaction processing
- Interactive web dashboard for visualization
- Health checks and model status monitoring

---

## **Technologies Used**

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Core programming language |
| **Flask** | Web framework for API and UI |
| **Scikit-learn** | Machine learning algorithms and preprocessing |
| **XGBoost** | Gradient boosting classifier |
| **Imbalanced-learn** | SMOTE and class imbalance handling |
| **Pandas & NumPy** | Data manipulation and numerical computing |
| **Matplotlib & Seaborn** | Data visualization |
| **Joblib** | Model serialization and persistence |
| **HTML, CSS, JavaScript** | Frontend design and interactivity |

---

## **Installation & Setup**

### **Prerequisites**
- Python 3.7 or higher
- pip package manager
- Virtual environment (recommended)

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd "Bank Fraud Detection 2"
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Usage**

### **Training the Model**
```bash
python src/train.py
```
This will:
- Load and preprocess the dataset
- Train supervised models (Random Forest, XGBoost)
- Train unsupervised models (Isolation Forest, One-Class SVM)
- Save trained models and preprocessors to disk

### **Running the Web Application**
```bash
python src/app.py
```
The API will be available at `http://localhost:5000`

### **Making Predictions**
Send a POST request to the `/predict` endpoint with transaction data:
```json
{
  "Amount": 150.50,
  "TransactionTime": "2025-12-26 14:30:00",
  "MerchantCategory": "Groceries",
  "Location": "New York",
  "UserId": "USER123",
  "DeviceType": "Mobile"
}
```

### **Health Check**
```bash
curl http://localhost:5000/health
```

---

## **Project Structure**

```
Bank Fraud Detection 2/
├── src/
│   ├── app.py                    # Flask application
│   ├── train.py                  # Model training script
│   ├── model_training.py         # Training utilities
│   ├── fraud_detector.py         # ML model definitions
│   ├── model_persistence.py      # Model save/load
│   ├── risk_scoring.py           # Risk calculation engine
│   ├── user_profiling.py         # User behavior analysis
│   ├── data_utils.py             # Data processing utilities
│   ├── evaluate_model.py         # Model evaluation
│   ├── diagnose_data.py          # Data diagnostics
│   ├── public/                   # Frontend files
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── models/                   # Saved models directory
│   └── plots/                    # Generated visualizations
├── data/
│   └── user_transaction_dataset.csv  # Training dataset
├── doc/
│   ├── 01_Abstract.md            # Project abstract
│   ├── 02_Introduction.md        # Introduction & background
│   ├── 03_Literature Review.md   # Literature review
│   ├── 04_EDA.md                 # Exploratory data analysis
│   ├── 05_Methodology.md         # Technical methodology
│   ├── 06_Results.md             # Results & discussion
│   └── 07_References.md          # References
├── tests/
│   ├── test_api.py               # API testing
│   └── test_transaction_handler.py # Handler testing
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── data.py                       # Data loading utilities
├── fraud-detection.ipynb         # Jupyter notebook analysis
└── logbook.md                    # Development logbook
```

---

## **Model Performance**

The system employs multiple models with ensemble methods:

- **Random Forest**: Excellent for capturing non-linear patterns
- **XGBoost**: Superior gradient boosting with feature importance
- **Isolation Forest**: Unsupervised anomaly detection for unknown fraud types
- **One-Class SVM**: Outlier detection for behavior deviations

Combined predictions provide robust fraud detection with high accuracy and minimal false positives.

---

## **Data Visualization**

The project includes comprehensive visualizations:
- Transaction amount distributions
- Fraud vs. legitimate transaction patterns
- Geographic heatmaps of transactions
- Temporal analysis of fraud occurrences
- Feature importance rankings
- Model performance metrics
- User behavior profiles

Sample visualizations are stored in the `plots/` directory.

---

## **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check and model status |
| `/predict` | POST | Predict fraud for a transaction |
| `/risk-score` | POST | Calculate detailed risk score |
| `/user-profile` | GET | Retrieve user spending profile |
| `/transaction-history` | GET | Get user transaction history |

---

## **Future Enhancements**

- Deep learning models (LSTM, Autoencoders) for sequence analysis
- Real-time model retraining with new fraudulent patterns
- Mobile application for push notifications
- Advanced visualization dashboards
- Integration with banking APIs
- Explainable AI (SHAP, LIME) for model interpretability
- Federated learning for privacy-preserving fraud detection

---

## **Team Members**

- **Sakshi Dadabhau Patil** - SYAIML-06 (231107004)
- **Tanisha Chudaman Badgujar** - SYAIML-26 (231107027)
- **Priyanshu Dipak Patil** - SYAIML-62 (241207003)
- **Chetan Prabhakar Sonawane** - SYAIML-39 (231107042)

---

## **References**

For detailed references and related research, see [07_References.md](doc/07_References.md)

---

## **License**

This project is developed as part of a semester project and is intended for educational purposes.

---

## **Support & Feedback**

For issues, questions, or suggestions, please refer to the documentation in the `doc/` folder or contact the project team.