import argparse
import sys
import data_loader as dl
import preprocessing as pp

def run_pipeline(file_path, label_path=None):
    """
    Main orchestration function for the healthcare fraud detection pipeline.
    """
    print(f"--- Starting Pipeline for {file_path} ---")
    
    # 1. Load Data
    df = dl.load_data(file_path, label_path=label_path)
    
    # 2. Preprocess Data
    df = pp.remove_duplicates(df)
    df = pp.handle_missing_values(df)
    df = pp.convert_date_columns(df)
    
    # Define ID columns to keep for output but drop from ML
    id_cols = ['ClaimID', 'Provider', 'PatientID', 'BeneID', 'AttendingPhysician', 'OperatingPhysician', 'OtherPhysician']
    
    # 3. Separate Features and Label
    X, y = pp.separate_features_and_label(df, target_col='PotentialFraud')
    
    # 4. Filter for ML Numeric Features
    X_ml = pp.get_ml_features(X, id_cols=id_cols)
    
    # 5. Save Cleaned Dataset
    output_path = "cleaned_claims.csv"
    df.to_csv(output_path, index=False)
    print(f"--- Pipeline Completed. Cleaned data saved to {output_path} ---")
    
    return X_ml, y

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Healthcare Fraud Detection Data Pipeline")
    parser.add_argument("--file", help="Path to the features CSV", default="Dataset/Train_Inpatientdata-1542865627584.csv")
    parser.add_argument("--labels", help="Path to the labels CSV", default="Dataset/Train-1542865627584.csv")
    
    args = parser.parse_args()
    
    try:
        X, y = run_pipeline(args.file, label_path=args.labels)
        print(f"Final ML Feature Set shape: {X.shape}")
        if y is not None:
            print(f"Target variable counts:\n{y.value_counts()}")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
