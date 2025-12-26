# Semester Project Logbook  

## Project Overview

The semester project focuses on building an **Intelligent Fraud Detection System** that analyzes financial transactions and classifies them as **Legitimate** or **Fraudulent** using **Machine Learning algorithms**.  
The system uses data preprocessing, feature engineering, class imbalance handling, ML model training, and a **Flask-based web application** for real-time fraud prediction.

---

## Week-wise Logbook Entries

---

### **Week 1: Problem Identification & Domain Study**
**Activities Performed:**
- Identified the problem of increasing fraud in digital financial transactions.
- Studied limitations of traditional rule-based fraud detection systems.
- Discussed project feasibility and scope with project guide.

**Outcome:**
- Finalized project domain: *Financial Fraud Detection using Machine Learning*.
- Defined high-level objectives and expected outcomes.

---

### **Week 2: Literature Survey & Requirement Analysis**
**Activities Performed:**
- Studied research papers and online resources on fraud detection.
- Analyzed existing ML-based fraud detection systems.
- Identified required hardware and software resources.

**Outcome:**
- Clear understanding of Machine Learning approaches for fraud detection.
- Finalized tools: Python, Flask, scikit-learn, pandas, NumPy.

---

### **Week 3: Dataset Collection & Understanding**
**Activities Performed:**
- Collected financial transaction dataset from Kaggle.
- Studied dataset attributes such as amount, category, merchant, time, and class labels.
- Identified class imbalance between fraud and non-fraud transactions.

**Outcome:**
- Dataset finalized for model training.
- Identified need for preprocessing and imbalance handling.

---

### **Week 4: Data Preprocessing**
**Activities Performed:**
- Cleaned dataset by handling missing and inconsistent values.
- Converted categorical features into numerical format.
- Normalized transaction amount values.

**Outcome:**
- Clean and structured dataset ready for feature engineering.
- Improved data quality for ML model training.

---

### **Week 5: Feature Engineering**
**Activities Performed:**
- Extracted time-based features such as hour, day, and month.
- Created behaviour-based features like spending patterns.
- Selected relevant features for model training.

**Outcome:**
- Feature-rich dataset that improves fraud detection accuracy.

---

### **Week 6: Handling Imbalanced Data**
**Activities Performed:**
- Analyzed class distribution between fraud and legitimate transactions.
- Applied SMOTE (Synthetic Minority Oversampling Technique).

**Outcome:**
- Balanced dataset with improved fraud class representation.
- Reduced bias towards majority class.

---

### **Week 7: Machine Learning Model Training**
**Activities Performed:**
- Implemented Random Forest Classifier.
- Trained Logistic Regression model.
- Applied Isolation Forest for anomaly detection.

**Outcome:**
- Multiple trained ML models for comparison.
- Initial performance metrics generated.

---

### **Week 8: Model Evaluation**
**Activities Performed:**
- Evaluated models using Accuracy, Precision, Recall, and F1-score.
- Generated confusion matrix.
- Compared model performance.

**Outcome:**
- Random Forest selected as final model due to better performance.
- Model ready for deployment.

---

### **Week 9: Model Saving & Integration**
**Activities Performed:**
- Saved trained model using pickle/joblib.
- Saved preprocessing objects (scaler, encoder).
- Prepared backend pipeline for real-time prediction.

**Outcome:**
- ML model artifacts ready for Flask integration.

---

### **Week 10: Flask Web Application Development**
**Activities Performed:**
- Designed Flask application structure.
- Created routes for homepage and prediction.
- Built HTML form for transaction input.

**Outcome:**
- Functional web interface for user interaction.

---

### **Week 11: Real-Time Fraud Prediction Integration**
**Activities Performed:**
- Integrated ML model with Flask backend.
- Implemented preprocessing pipeline for user input.
- Displayed fraud probability and result on result page.

**Outcome:**
- End-to-end fraud detection system working successfully.

---

### **Week 12: Testing & Result Analysis**
**Activities Performed:**
- Tested system with multiple transaction scenarios.
- Verified predictions for low-risk and high-risk transactions.
- Analyzed model behavior and edge cases.

**Outcome:**
- System produces accurate and consistent fraud predictions.
- Verified real-time performance.

---

### **Week 13: Documentation & Report Preparation**
**Activities Performed:**
- Prepared project report including diagrams and screenshots.
- Documented algorithms, system architecture, and results.
- Compiled bibliography and references.

**Outcome:**
- Complete project documentation prepared.

---

### **Week 14: Final Review & Submission**
**Activities Performed:**
- Reviewed project with guide.
- Made final corrections and formatting changes.
- Submitted project report and source code.

**Outcome:**
- Successful completion of semester project.

---

## Tools & Technologies Used

- **Programming Language:** Python  
- **ML Libraries:** scikit-learn, pandas, NumPy  
- **Web Framework:** Flask  
- **Visualization:** matplotlib, seaborn  
- **Dataset Source:** Kaggle  
- **Development Tools:** VS Code, Jupyter Notebook  



