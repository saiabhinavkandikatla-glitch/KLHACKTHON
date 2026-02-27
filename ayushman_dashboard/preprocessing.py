import pandas as pd
import numpy as np

def remove_duplicates(df):
    """Removes duplicate rows from the DataFrame."""
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    print(f"Removed {initial_count - final_count} duplicate rows.")
    return df

def handle_missing_values(df):
    """Handles null values by dropping rows with missing essential data or filling others."""
    # For a hackathon-ready version, we'll do a simple fill/drop strategy
    # Drop rows where PotentialFraud is missing since that's our target
    if 'PotentialFraud' in df.columns:
        df = df.dropna(subset=['PotentialFraud'])
    
    # Fill numeric columns with median, categorical with mode
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
            
    print("Handled missing values using simple imputation (median/mode).")
    return df

def convert_date_columns(df):
    """Automatically detects and converts date-like columns to datetime objects."""
    for col in df.columns:
        # Check if column name contains 'Date' or 'Year' or 'Month'
        if any(keyword in col.lower() for keyword in ['date', 'year', 'month']):
            try:
                df[col] = pd.to_datetime(df[col])
                print(f"Converted column '{col}' to datetime.")
            except (ValueError, TypeError):
                # If conversion fails, just skip it
                pass
    return df

def separate_features_and_label(df, target_col='PotentialFraud'):
    """Splits the dataset into features X and label y."""
    if target_col not in df.columns:
        print(f"Warning: Target column '{target_col}' not found.")
        return df, None
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Map 'Yes'/'No' labels to 1/0 if present
    if y.dtype == 'object':
        y = y.map({'Yes': 1, 'No': 0, '1': 1, '0': 0})
        
    print(f"Separated features and target '{target_col}'.")
    return X, y

def get_ml_features(X, id_cols=None):
    """
    Automatically detects numeric columns for ML and excludes ID columns.
    
    Args:
        X (pd.DataFrame): The feature dataframe.
        id_cols (list): List of columns to exclude from ML input.
        
    Returns:
        pd.DataFrame: Cleaned feature set ready for ML.
    """
    if id_cols is None:
        id_cols = []
        
    # Exclude ID columns
    ml_input = X.drop(columns=[col for col in id_cols if col in X.columns])
    
    # Select only numeric columns
    numeric_features = ml_input.select_dtypes(include=['int64', 'float64'])
    
    print(f"Detected {len(numeric_features.columns)} numeric features for ML.")
    return numeric_features
