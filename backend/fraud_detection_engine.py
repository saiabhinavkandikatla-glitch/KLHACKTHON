#!/usr/bin/env python3
"""
Hospital-Level Fraud Detection Engine for Healthcare Claims
===========================================================

This module implements an Isolation Forest-based anomaly detection system
for identifying potentially fraudulent healthcare claims at the provider level.

Author: Fraud Detection Team
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# STEP 1: Load Dataset
# =============================================================================

def load_data(filepath='cleaned_claims.csv'):
    """
    Load and validate the cleaned claims dataset.
    
    Parameters:
    -----------
    filepath : str
        Path to the cleaned claims CSV file
        
    Returns:
    --------
    pd.DataFrame
        Loaded and validated dataframe with PotentialFraud converted to binary
        
    Raises:
    -------
    FileNotFoundError
        If the specified file does not exist
    ValueError
        If required columns are missing
    """
    print("=" * 60)
    print("STEP 1: Loading Dataset")
    print("=" * 60)
    
    # Load the dataset
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Successfully loaded {filepath}")
        print(f"  - Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {filepath}")
    
    # Validate required columns exist
    required_columns = ['Provider', 'InscClaimAmtReimbursed', 'PotentialFraud']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    print(f"✓ Required columns validated")
    
    # Convert PotentialFraud from Yes/No to 1/0
    # This is our ground truth label for evaluation (not used in training)
    df['PotentialFraud'] = df['PotentialFraud'].map({'Yes': 1, 'No': 0})
    fraud_count = df['PotentialFraud'].sum()
    print(f"✓ Converted PotentialFraud to binary (1/0)")
    print(f"  - Fraudulent claims: {fraud_count:,} ({fraud_count/len(df)*100:.2f}%)")
    print(f"  - Normal claims: {len(df) - fraud_count:,} ({(len(df)-fraud_count)/len(df)*100:.2f}%)")
    
    return df


# =============================================================================
# STEP 2: Feature Engineering
# =============================================================================

def engineer_features(df):
    """
    Perform comprehensive feature engineering for fraud detection.
    
    Creates provider-level aggregates, peer comparisons, procedure frequencies,
    and chronic condition counts to capture anomalous patterns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with raw claim data
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with engineered features merged
    """
    print("\n" + "=" * 60)
    print("STEP 2: Feature Engineering")
    print("=" * 60)
    
    df = df.copy()
    
    # -------------------------------------------------------------------------
    # 2.1 Provider-Level Aggregates
    # -------------------------------------------------------------------------
    print("\n2.1 Computing Provider-Level Aggregates...")
    
    provider_stats = df.groupby('Provider').agg({
        'InscClaimAmtReimbursed': ['mean', 'count'],
        'PotentialFraud': 'mean'  # For validation only
    }).reset_index()
    
    # Flatten column names
    provider_stats.columns = ['Provider', 'ProviderAvgClaimAmount', 
                              'ProviderClaimCount', 'ProviderFraudRate']
    
    # Merge back to main dataframe
    df = df.merge(provider_stats, on='Provider', how='left')
    print(f"  ✓ ProviderAvgClaimAmount: Average claim amount per provider")
    print(f"  ✓ ProviderClaimCount: Number of claims per provider")
    print(f"  ✓ ProviderFraudRate: Historical fraud rate per provider (validation only)")
    
    # -------------------------------------------------------------------------
    # 2.2 Peer Average Comparison
    # -------------------------------------------------------------------------
    print("\n2.2 Computing Peer Average Comparison...")
    
    # Global average claim amount across all providers
    global_avg = df['InscClaimAmtReimbursed'].mean()
    df['GlobalAvgClaimAmount'] = global_avg
    df['ClaimAmountDeviation'] = df['InscClaimAmtReimbursed'] - global_avg
    
    print(f"  ✓ GlobalAvgClaimAmount: ${global_avg:,.2f}")
    print(f"  ✓ ClaimAmountDeviation: Deviation from global average")
    
    # -------------------------------------------------------------------------
    # 2.3 Procedure Frequency per Provider
    # -------------------------------------------------------------------------
    print("\n2.3 Computing Procedure Frequency per Provider...")
    
    # Check if procedure code column exists
    procedure_col = 'ClmProcedureCode_1'
    if procedure_col in df.columns:
        # Count frequency of each procedure per provider
        procedure_freq = df.groupby(['Provider', procedure_col]).size().reset_index(name='ProcedureFrequency')
        
        # Merge back to main dataframe
        df = df.merge(procedure_freq, on=['Provider', procedure_col], how='left')
        print(f"  ✓ ProcedureFrequency: How often each provider uses specific procedures")
    else:
        # If procedure column doesn't exist, set frequency to 1 (neutral)
        df['ProcedureFrequency'] = 1
        print(f"  ⚠ {procedure_col} not found, using default value")
    
    # -------------------------------------------------------------------------
    # 2.4 Chronic Condition Count
    # -------------------------------------------------------------------------
    print("\n2.4 Computing Chronic Condition Count...")
    
    # Identify all chronic condition columns
    chronic_cols = [col for col in df.columns if col.startswith('ChronicCond_')]
    
    if chronic_cols:
        # Sum all chronic condition indicators for each patient
        df['TotalChronicConditions'] = df[chronic_cols].sum(axis=1)
        print(f"  ✓ TotalChronicConditions: Sum of {len(chronic_cols)} chronic condition indicators")
        print(f"    Average conditions per claim: {df['TotalChronicConditions'].mean():.2f}")
    else:
        # If no chronic condition columns, set to 0
        df['TotalChronicConditions'] = 0
        print(f"  ⚠ No ChronicCond_ columns found, using default value")
    
    print(f"\n✓ Feature engineering complete")
    print(f"  - Final dataframe shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    return df


# =============================================================================
# STEP 3 & 4: Feature Selection and Scaling
# =============================================================================

def select_and_scale_features(df):
    """
    Select relevant numeric features and apply StandardScaler.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with engineered features
        
    Returns:
    --------
    tuple
        (scaled_features_array, feature_columns_list, fitted_scaler)
    """
    print("\n" + "=" * 60)
    print("STEP 3 & 4: Feature Selection and Scaling")
    print("=" * 60)
    
    # Define features for anomaly detection
    # These are numeric indicators that could signal fraudulent behavior
    feature_columns = [
        'InscClaimAmtReimbursed',      # Claim amount (unusual amounts are suspicious)
        'ClaimDurationInDays',          # Duration of claim processing
        'ProviderAvgClaimAmount',       # Provider's average claim amount
        'ProviderClaimCount',           # Provider's claim volume
        'ClaimAmountDeviation',         # Deviation from global average
        'ProcedureFrequency',           # How often provider uses procedures
        'TotalChronicConditions',       # Patient's chronic condition burden
        'IPAnnualReimbursementAmt',     # Inpatient annual reimbursement
        'OPAnnualReimbursementAmt'      # Outpatient annual reimbursement
    ]
    
    # Add optional columns if they exist
    optional_columns = ['AdmissionDurationInDays', 'Age']
    for col in optional_columns:
        if col in df.columns:
            feature_columns.append(col)
            print(f"✓ Including optional feature: {col}")
    
    # Filter to only columns that exist in the dataframe
    available_features = [col for col in feature_columns if col in df.columns]
    missing_features = [col for col in feature_columns if col not in df.columns]
    
    if missing_features:
        print(f"⚠ Missing features (will be excluded): {missing_features}")
    
    print(f"\n✓ Selected {len(available_features)} features for modeling:")
    for i, feature in enumerate(available_features, 1):
        print(f"  {i}. {feature}")
    
    # Extract feature matrix
    X = df[available_features].copy()
    
    # Handle any missing values by filling with median
    # (Isolation Forest cannot handle NaN values)
    missing_count = X.isnull().sum().sum()
    if missing_count > 0:
        X = X.fillna(X.median())
        print(f"\n⚠ Filled {missing_count} missing values with median")
    
    # Apply StandardScaler to normalize features
    # This ensures all features contribute equally to distance calculations
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"\n✓ Applied StandardScaler normalization")
    print(f"  - Mean of scaled features: ~0")
    print(f"  - Std of scaled features: ~1")
    
    return X_scaled, available_features, scaler


# =============================================================================
# STEP 5: Isolation Forest Model Training
# =============================================================================

def train_isolation_model(X_scaled, df):
    """
    Train Isolation Forest model for anomaly detection.
    
    The contamination parameter is set based on the actual fraud ratio
    in the dataset, capped at 25% to avoid over-aggressive flagging.
    
    Parameters:
    -----------
    X_scaled : np.ndarray
        Scaled feature matrix
    df : pd.DataFrame
        Original dataframe with PotentialFraud column
        
    Returns:
    --------
    tuple
        (trained_model, anomaly_scores, anomaly_flags)
    """
    print("\n" + "=" * 60)
    print("STEP 5: Isolation Forest Model Training")
    print("=" * 60)
    
    # Calculate fraud ratio from ground truth
    # This helps set appropriate contamination level
    fraud_ratio = df['PotentialFraud'].mean()
    contamination = min(0.25, fraud_ratio)  # Cap at 25% to be conservative
    
    print(f"✓ Calculated fraud ratio: {fraud_ratio:.4f} ({fraud_ratio*100:.2f}%)")
    print(f"✓ Setting contamination parameter: {contamination:.4f}")
    
    # Initialize Isolation Forest
    # n_estimators=200 provides good balance of accuracy and speed
    # random_state=42 ensures reproducibility
    iso_forest = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,  # Use all available CPU cores
        verbose=0
    )
    
    print(f"\n✓ Training Isolation Forest...")
    print(f"  - n_estimators: 200")
    print(f"  - contamination: {contamination:.4f}")
    print(f"  - random_state: 42")
    
    # Fit the model
    iso_forest.fit(X_scaled)
    
    # Generate anomaly scores (decision_function)
    # Negative values indicate anomalies, positive values indicate normal
    anomaly_scores = iso_forest.decision_function(X_scaled)
    
    # Generate anomaly flags (-1 for anomaly, 1 for normal)
    anomaly_flags_raw = iso_forest.predict(X_scaled)
    
    # Convert to binary (1 = fraud/anomaly, 0 = normal)
    # This matches the PotentialFraud encoding (1 = fraud, 0 = normal)
    anomaly_flags = np.where(anomaly_flags_raw == -1, 1, 0)
    
    # Statistics
    flagged_count = anomaly_flags.sum()
    print(f"\n✓ Model training complete")
    print(f"  - Claims flagged as anomalous: {flagged_count:,} ({flagged_count/len(df)*100:.2f}%)")
    print(f"  - Claims classified as normal: {len(df) - flagged_count:,} ({(len(df)-flagged_count)/len(df)*100:.2f}%)")
    
    return iso_forest, anomaly_scores, anomaly_flags


# =============================================================================
# STEP 6: Risk Score Normalization
# =============================================================================

def compute_risk_scores(anomaly_scores):
    """
    Convert anomaly scores to 0-100 RiskScore scale.
    
    Higher scores indicate higher fraud risk.
    The transformation inverts and scales the anomaly scores so that
    more negative anomaly scores (more anomalous) become higher risk scores.
    
    Parameters:
    -----------
    anomaly_scores : np.ndarray
        Raw anomaly scores from Isolation Forest
        
    Returns:
    --------
    np.ndarray
        Normalized risk scores (0-100 scale)
    """
    print("\n" + "=" * 60)
    print("STEP 6: Risk Score Normalization")
    print("=" * 60)
    
    # Anomaly scores are typically in range [-0.5, 0.5]
    # More negative = more anomalous = higher risk
    
    # Min-max scaling to 0-100 range
    # We invert so that higher scores = higher risk
    min_score = anomaly_scores.min()
    max_score = anomaly_scores.max()
    
    # Invert and scale: (max - score) / (max - min) * 100
    risk_scores = ((max_score - anomaly_scores) / (max_score - min_score)) * 100
    
    print(f"✓ Converted anomaly scores to 0-100 RiskScore")
    print(f"  - Original score range: [{min_score:.4f}, {max_score:.4f}]")
    print(f"  - Risk score range: [{risk_scores.min():.2f}, {risk_scores.max():.2f}]")
    print(f"  - Mean risk score: {risk_scores.mean():.2f}")
    
    return risk_scores


# =============================================================================
# STEP 7: Provider-Level Risk Aggregation
# =============================================================================

def aggregate_provider_risk(df, risk_scores, anomaly_flags):
    """
    Aggregate risk metrics at the provider level.
    
    This helps identify which hospitals have the highest fraud risk
    based on their claims patterns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Original dataframe with Provider column
    risk_scores : np.ndarray
        Normalized risk scores for each claim
    anomaly_flags : np.ndarray
        Binary anomaly flags for each claim
        
    Returns:
    --------
    pd.DataFrame
        Provider-level risk summary
    """
    print("\n" + "=" * 60)
    print("STEP 7: Provider-Level Risk Aggregation")
    print("=" * 60)
    
    # Add risk scores and flags to dataframe
    df = df.copy()
    df['RiskScore'] = risk_scores
    df['AnomalyFlag'] = anomaly_flags
    
    # Aggregate by provider
    provider_risk = df.groupby('Provider').agg({
        'RiskScore': 'mean',                    # Average risk score
        'AnomalyFlag': ['sum', 'count'],        # Suspicious claims and total claims
        'PotentialFraud': 'sum'                 # Actual fraud count (for validation)
    }).reset_index()
    
    # Flatten column names
    provider_risk.columns = ['Provider', 'AvgRiskScore', 
                             'SuspiciousClaimCount', 'TotalClaims', 'ActualFraudCount']
    
    # Calculate suspicious claim percentage
    provider_risk['SuspiciousClaimPercentage'] = (
        provider_risk['SuspiciousClaimCount'] / provider_risk['TotalClaims'] * 100
    )
    
    # Sort by average risk score (descending)
    provider_risk = provider_risk.sort_values('AvgRiskScore', ascending=False)
    
    print(f"✓ Aggregated risk metrics for {len(provider_risk)} providers")
    print(f"\nTop 5 Highest Risk Providers:")
    print(provider_risk.head().to_string())
    
    print(f"\nRisk Score Statistics:")
    print(f"  - Highest risk provider: {provider_risk['AvgRiskScore'].max():.2f}")
    print(f"  - Lowest risk provider: {provider_risk['AvgRiskScore'].min():.2f}")
    print(f"  - Average risk across providers: {provider_risk['AvgRiskScore'].mean():.2f}")
    
    # Select and reorder final columns
    provider_risk = provider_risk[[
        'Provider', 'AvgRiskScore', 'SuspiciousClaimPercentage', 
        'TotalClaims', 'SuspiciousClaimCount', 'ActualFraudCount'
    ]]
    
    return provider_risk


# =============================================================================
# STEP 8: Model Evaluation
# =============================================================================

def evaluate_model(df, anomaly_flags):
    """
    Evaluate anomaly detection performance against ground truth.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with PotentialFraud ground truth labels
    anomaly_flags : np.ndarray
        Predicted anomaly flags
        
    Returns:
    --------
    dict
        Dictionary containing evaluation metrics
    """
    print("\n" + "=" * 60)
    print("STEP 8: Model Evaluation")
    print("=" * 60)
    
    # Ground truth
    y_true = df['PotentialFraud'].values
    y_pred = anomaly_flags
    
    # Confusion Matrix
    # Format: [[TN, FP], [FN, TP]]
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("Confusion Matrix:")
    print(f"                 Predicted")
    print(f"                 Normal  Fraud")
    print(f"Actual Normal    {tn:6d}  {fp:6d}  (Specificity: {tn/(tn+fp)*100:.2f}%)")
    print(f"       Fraud     {fn:6d}  {tp:6d}  (Sensitivity: {tp/(tp+fn)*100:.2f}%)")
    
    # Calculate metrics
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    # Accuracy
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    
    print(f"\nPerformance Metrics:")
    print(f"  ✓ Accuracy:  {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"  ✓ Precision: {precision:.4f}  ({precision*100:.2f}%)")
    print(f"  ✓ Recall:    {recall:.4f}  ({recall*100:.2f}%)")
    print(f"  ✓ F1-Score:  {f1:.4f}  ({f1*100:.2f}%)")
    
    # Interpretation
    print(f"\nInterpretation:")
    print(f"  - Precision: Of all claims flagged as fraud, {precision*100:.1f}% were actually fraudulent")
    print(f"  - Recall: Of all actual fraudulent claims, {recall*100:.1f}% were detected")
    print(f"  - F1-Score: Harmonic mean of precision and recall")
    
    metrics = {
        'confusion_matrix': cm,
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn,
        'true_positives': tp,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
    
    return metrics

# =============================================================================
# MAIN EXECUTION PIPELINE
# =============================================================================

def run_pipeline(data_path="cleaned_claims.csv"):
    df = load_data(data_path)
    
    # Step 2: Feature Engineering
    df_engineered = engineer_features(df)
    
    # Step 3 & 4: Feature Selection + Scaling
    X_scaled, feature_cols, scaler = select_and_scale_features(df_engineered)
    
    # Step 5: Train Isolation Model
    model, anomaly_scores, anomaly_flags = train_isolation_model(X_scaled, df_engineered)
    
    # Step 6: Compute Risk Scores
    risk_scores = compute_risk_scores(anomaly_scores)
    
    # Step 7: Provider Aggregation
    provider_summary = aggregate_provider_risk(df_engineered, risk_scores, anomaly_flags)
    
    # Step 8: Evaluate Model
    metrics = evaluate_model(df_engineered, anomaly_flags)
    
    # Save outputs
    print("\n💾 Saving output files...")
    
    df_engineered["RiskScore"] = risk_scores
    df_engineered["AnomalyFlag"] = anomaly_flags
    
    # df_engineered.to_csv("claim_level_results.csv", index=False)
    # provider_summary.to_csv("provider_risk_summary.csv", index=False)
    return {
        "df": df_engineered,
        "provider_summary": provider_summary,
        "metrics": metrics
    }
