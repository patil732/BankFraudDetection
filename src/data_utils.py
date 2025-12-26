import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.categorical_cols = None
        self.numerical_cols = None

    def load_data(self, filepath):
        """Load and standardize the dataset"""
        print(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)

        # -------- STANDARDIZE COLUMN NAMES --------
        df.rename(columns={
            'transaction_id': 'Transaction_ID',
            'user_id': 'User_ID',
            'transaction_datetime': 'Transaction_Time',
            'amount': 'Transaction_Amount',
            'merchant_category': 'Merchant_Category',
            'transaction_channel': 'Transaction_Channel',
            'device_type': 'Device_Type',
            'location': 'Location',
            'is_fraud': 'Is_Fraudulent'
        }, inplace=True)
        # ------------------------------------------

        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nData types:\n{df.dtypes}")
        print(f"\nMissing values:\n{df.isnull().sum()}")

        print("\nClass distribution:")
        print(df['Is_Fraudulent'].value_counts(normalize=True))

        return df

    def analyze_features(self, df):
        """Identify categorical and numerical features"""
        categorical_cols = []
        numerical_cols = []

        for col in df.columns:
            if col in ['Transaction_ID', 'Is_Fraudulent']:
                continue
            if df[col].dtype == 'object':
                categorical_cols.append(col)
            else:
                numerical_cols.append(col)

        self.categorical_cols = categorical_cols
        self.numerical_cols = numerical_cols

        print(f"Categorical columns: {categorical_cols}")
        print(f"Numerical columns: {numerical_cols}")

        return categorical_cols, numerical_cols

    def feature_engineering(self, df):
        """Create ML-ready features"""
        df_eng = df.copy()

        # -------- DATETIME PARSING (FIXED) --------
        df_eng['Transaction_Time'] = pd.to_datetime(
            df_eng['Transaction_Time'],
            dayfirst=True,
            errors='coerce'
        )

        # Drop invalid datetime rows
        df_eng = df_eng.dropna(subset=['Transaction_Time'])

        # -------- TIME FEATURES --------
        df_eng['Hour'] = df_eng['Transaction_Time'].dt.hour
        df_eng['DayOfWeek'] = df_eng['Transaction_Time'].dt.dayofweek
        df_eng['Is_Weekend'] = df_eng['DayOfWeek'].isin([5, 6]).astype(int)
        df_eng['Is_Night'] = ((df_eng['Hour'] >= 0) & (df_eng['Hour'] <= 6)).astype(int)

        # ⛔ IMPORTANT: REMOVE DATETIME COLUMN
        df_eng = df_eng.drop(columns=['Transaction_Time'])

        # -------- USER BEHAVIOR FEATURES --------
        user_stats = df_eng.groupby('User_ID').agg({
            'Transaction_Amount': ['mean', 'std', 'count']
        }).reset_index()

        user_stats.columns = [
            'User_ID',
            'User_Avg_Amount',
            'User_Std_Amount',
            'User_Transaction_Count'
        ]

        df_eng = pd.merge(df_eng, user_stats, on='User_ID', how='left')

        # -------- AMOUNT FEATURES --------
        df_eng['Amount_Log'] = np.log1p(df_eng['Transaction_Amount'])
        df_eng['Amount_to_Avg_Ratio'] = (
            df_eng['Transaction_Amount'] / (df_eng['User_Avg_Amount'] + 1)
        )

        return df_eng

    def prepare_data(self, df, test_size=0.2, validate_size=0.1):
        """Prepare train, validation, and test splits"""
        X = df.drop(['Transaction_ID', 'Is_Fraudulent'], axis=1)
        y = df['Is_Fraudulent']

        # Train + Val vs Test
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=self.random_state,
            stratify=y
        )

        # Train vs Validation
        val_ratio = validate_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val,
            test_size=val_ratio,
            random_state=self.random_state,
            stratify=y_train_val
        )

        print(f"Training set: {X_train.shape}")
        print(f"Validation set: {X_val.shape}")
        print(f"Test set: {X_test.shape}")
        print("\nTraining class distribution:")
        print(y_train.value_counts(normalize=True))

        return X_train, X_val, X_test, y_train, y_val, y_test
