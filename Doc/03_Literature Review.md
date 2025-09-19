# Literature Review  

## 1. Summary of Existing Technologies, Methods, and Solutions  

### 1.1 Rule-Based Fraud Detection Systems  
Early fraud detection systems relied on **rule-based approaches**, where predefined thresholds (e.g., transaction amount limits, blacklisted IP addresses, unusual geolocation) were used to flag anomalies.  

**Advantages:**  
- Simple to implement.  
- Transparent decision-making process.  

**Limitations:**  
- Inflexible and unable to adapt to evolving fraud tactics.  
- High false-positive rates (genuine transactions often flagged as fraud).  
- Cannot model complex user behavior.  

---

### 1.2 Statistical and Data Mining Approaches  
With the rise of data-driven methods, probabilistic models and statistical techniques such as **Logistic Regression** and **Bayesian Networks** were applied to fraud detection.  

**Advantages:**  
- Provide interpretability and probabilistic insights.  
- Capture correlations between transaction features.  

**Limitations:**  
- Limited in handling large-scale, high-dimensional data.  
- Require strong assumptions about feature distributions.  

---

### 1.3 Machine Learning for Fraud Detection  
The introduction of **supervised learning models** significantly improved fraud detection performance.  

**Commonly used algorithms include:**  
- **Decision Trees & Random Forests** – Handle non-linear relationships and imbalanced data.  
- **Gradient Boosting & XGBoost** – Deliver high predictive accuracy with ensemble methods.  
- **Neural Networks** – Capture complex transaction patterns.  

**Challenges:**  
- Fraud datasets are highly imbalanced (fraudulent cases are rare).  
- Risk of overfitting on historical fraud patterns.  

**Solutions in Literature:**  
- **SMOTE (Synthetic Minority Oversampling Technique)** to balance datasets.  
- **Cost-sensitive learning** to penalize misclassification of fraud cases.  

---

### 1.4 Unsupervised and Anomaly Detection Methods  
To detect new or evolving fraud patterns, researchers have applied **unsupervised learning** and **anomaly detection techniques**:  
- **K-Means, DBSCAN** – Cluster transactions and detect outliers.  
- **Isolation Forest** – Identifies anomalies by isolating rare behaviors.  
- **One-Class SVM** – Learns a boundary around normal transactions to detect deviations.  

**Advantages:**  
- No need for labeled fraud data.  
- Useful for detecting novel fraud strategies.  

**Limitations:**  
- Higher false alarm rates if features are not well-defined.  
- Sensitive to parameter selection.  

---

### 1.5 Hybrid Fraud Detection Models  
Recent studies emphasize **hybrid approaches**, combining supervised and unsupervised learning:  
- **Supervised Models** – Effective for detecting known fraud types.  
- **Anomaly Detection Models** – Capture new or evolving fraud tactics.  
- **Behavioral Features** – Incorporating temporal, spatial, and user-specific spending patterns enhances accuracy.  

**Research Trend:**  
- Focus on **real-time fraud detection systems** capable of handling high transaction volumes.  
- Integration with **big data platforms and cloud services** for scalability.  

---

## 2. Why Machine Learning for This Project?  

Based on the literature review, this project adopts a **Machine Learning-driven hybrid approach** for fraud detection because:  

- **Adaptability** – ML models learn evolving fraud tactics better than static rules.  
- **Higher Accuracy** – Supervised classifiers (**Random Forest, XGBoost**) reduce false negatives.  
- **Novel Fraud Detection** – Anomaly detection (**Isolation Forest, One-Class SVM**) identifies previously unseen fraud patterns.  
- **Behavior Awareness** – Dynamic user-specific profiles reduce false positives by considering spending habits, geolocation, and transaction frequency.  
- **Real-Time Application** – Integration with streaming systems enables instant fraud alerts.  

**Key Model Choices for This Project:**  
- **Supervised Models**: Random Forest, XGBoost for classification of labeled fraud data.  
- **Unsupervised Models**: Isolation Forest, One-Class SVM for anomaly detection.  
- **Feature Engineering**: Temporal (time of transaction), spatial (geolocation), behavioral (spending patterns).  
- **Deployment**: Scalable real-time system with alert mechanisms and personalized financial insights.  
