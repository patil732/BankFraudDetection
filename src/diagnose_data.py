#!/usr/bin/env python3
"""
Diagnose data issues and suggest fixes
"""
import pandas as pd
import numpy as np
import os

def diagnose_data(filepath):
    print("="*80)
    print("🔍 DATA DIAGNOSIS REPORT")
    print("="*80)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    print(f"\n📊 BASIC INFO:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    
    print(f"\n🔢 DATA TYPES:")
    for col in df.columns:
        print(f"   {col:<30}: {df[col].dtype}")
    
    print(f"\n📈 MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ No missing values found")
    else:
        for col, count in missing[missing > 0].items():
            percentage = (count / len(df)) * 100
            print(f"   ⚠️  {col:<30}: {count} ({percentage:.2f}%)")
    
    # -------- TARGET VARIABLE CHECK --------
    print(f"\n🎯 TARGET VARIABLE ANALYSIS:")
    fraud_cols = [c for c in df.columns if 'fraud' in c.lower()]
    
    if fraud_cols:
        target_col = fraud_cols[0]
        fraud_counts = df[target_col].value_counts()
        fraud_percentage = (fraud_counts.get(1, 0) / len(df)) * 100
        
        print(f"   Target column: {target_col}")
        print(f"   Fraud cases: {fraud_counts.get(1, 0)}")
        print(f"   Non-fraud cases: {fraud_counts.get(0, 0)}")
        print(f"   Fraud percentage: {fraud_percentage:.2f}%")
        
        if fraud_percentage < 1:
            print("   ⚠️  VERY IMBALANCED (<1%)")
        elif fraud_percentage < 5:
            print("   ⚠️  HIGHLY IMBALANCED (<5%)")
        elif fraud_percentage < 20:
            print("   ⚠️  IMBALANCED (<20%)")
        else:
            print("   ✅ Reasonably balanced dataset")
    else:
        print("   ❌ No fraud label column detected")
    
    # -------- FEATURE DISTRIBUTION --------
    print(f"\n📊 NUMERIC FEATURE SUMMARY:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:10]:
        print(
            f"   {col:<30}: "
            f"min={df[col].min():.2f}, "
            f"max={df[col].max():.2f}, "
            f"mean={df[col].mean():.2f}"
        )
    
    # -------- RECOMMENDATIONS --------
    print(f"\n💡 RECOMMENDATIONS:")
    
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        print(f"   1. Remove constant columns: {constant_cols}")
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        high_corr = [
            (corr_matrix.columns[i], corr_matrix.columns[j])
            for i in range(len(corr_matrix.columns))
            for j in range(i+1, len(corr_matrix.columns))
            if corr_matrix.iloc[i, j] > 0.95
        ]
        if high_corr:
            print(f"   2. Highly correlated features (sample): {high_corr[:5]}")
    
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"   3. Remove {duplicates} duplicate rows")
    
    print(f"\n✅ DIAGNOSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    # -------- FIXED DATA PATH --------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    data_file = os.path.join(PROJECT_ROOT, "data", "user_transaction_dataset.csv")
    
    diagnose_data(data_file)
