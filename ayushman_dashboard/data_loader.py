import pandas as pd
import os
import sys

def load_data(file_path, label_path=None):
    """
    Loads one or more CSV files. If label_path is provided, it merges the data with labels.
    
    Args:
        file_path (str): Path to the features CSV file (e.g., Inpatient data).
        label_path (str, optional): Path to the labels CSV file.
        
    Returns:
        pd.DataFrame: The loaded (and potentially merged) dataset.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        sys.exit(1)
    
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} rows from {file_path}")
        
        if label_path:
            if not os.path.exists(label_path):
                print(f"Warning: Label file {label_path} not found. Proceeding without labels.")
            else:
                labels = pd.read_csv(label_path)
                # Merge on Provider as it's the common link in this specific Kaggle dataset
                df = pd.merge(df, labels, on='Provider', how='left')
                print(f"Merged with labels from {label_path}. New shape: {df.shape}")
        
        return df
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Simple test for the loader
    if len(sys.argv) > 1:
        load_data(sys.argv[1])
    else:
        print("Usage: python data_loader.py <file_path>")
