import pandas as pd
import numpy as np
import random
import uuid
import os

def load_mock_data():
    np.random.seed(42)
    random.seed(42)
    
    n_records = 10000
    
    # Load base Kaggle dataset
    csv_path = os.path.join(os.path.dirname(__file__), 'insurance.csv')
    try:
        base_df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("Warning: insurance.csv not found. Falling back to synthetic generation.")
        base_df = None
        
    # Generate static mappings
    states = ['Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Tamil Nadu', 'Gujarat', 
              'Kerala', 'Rajasthan', 'Madhya Pradesh', 'Bihar', 'West Bengal']
    elevated_states = ['Bihar', 'Uttar Pradesh']
    
    hospitals = [f'HOSP_{i:04d}' for i in range(1, 101)]
    high_risk_hospitals = ['HOSP_0013', 'HOSP_0042', 'HOSP_0077', 'HOSP_0099']
    
    procedures = [f'PROC_{i:03d}' for i in range(1, 51)]
    
    # Map each hospital to a state to ensure consistency
    hospital_to_state = {h: np.random.choice(states) for h in hospitals}
    
    claim_ids = [f'CLM_{uuid.uuid4().hex[:8].upper()}' for _ in range(n_records)]
    hospital_assignments = np.random.choice(hospitals, n_records)
    state_assignments = [hospital_to_state[h] for h in hospital_assignments]
    procedure_assignments = np.random.choice(procedures, n_records)
    
    if base_df is not None and not base_df.empty:
        # Sample with replacement from the kaggle dataset to get 10k records
        sampled_df = base_df.sample(n=n_records, replace=True, random_state=42).reset_index(drop=True)
        # Use the 'charges' column for claim_amount
        claim_amounts = np.round(sampled_df['charges'].values, 2)
    else:
        # Log-normal distribution for claim amounts as fallback
        claim_amounts = np.random.lognormal(mean=9., sigma=1., size=n_records)
        claim_amounts = np.round(claim_amounts, 2)
    
    # Initialize flags and scores
    image_reuse_flag = np.zeros(n_records, dtype=int)
    duplicate_flag = np.zeros(n_records, dtype=int)
    anomaly_scores = np.random.uniform(0, 0.3, n_records)
    risk_scores = np.zeros(n_records)
    
    # Target 5% image reuse overall
    image_reuse_indices = np.random.choice(n_records, int(0.05 * n_records), replace=False)
    image_reuse_flag[image_reuse_indices] = 1
    
    # ~5% duplicate claims
    duplicate_indices = np.random.choice(n_records, int(0.05 * n_records), replace=False)
    duplicate_flag[duplicate_indices] = 1
    
    # Calculate risk scores based on rules
    for i in range(n_records):
        hosp = hospital_assignments[i]
        st = state_assignments[i]
        
        # Base risk for normal claims
        base_risk = random.uniform(0, 20)
        
        has_fraud_flag = False
        
        if image_reuse_flag[i] == 1:
            base_risk += random.uniform(40, 60)
            anomaly_scores[i] = max(anomaly_scores[i], random.uniform(0.7, 0.95))
            has_fraud_flag = True
            
        if duplicate_flag[i] == 1:
            base_risk += random.uniform(30, 50)
            anomaly_scores[i] = max(anomaly_scores[i], random.uniform(0.6, 0.9))
            has_fraud_flag = True
            
        if hosp in high_risk_hospitals:
            # High risk hospitals have a 30% chance of generating a high risk claim even without direct flags
            if random.random() < 0.3 and not has_fraud_flag:
                base_risk += random.uniform(50, 70)
                anomaly_scores[i] = max(anomaly_scores[i], random.uniform(0.7, 0.9))
                
        if st in elevated_states:
            # Elevated states have slightly higher average risk
            base_risk += random.uniform(10, 20)
            
        # Add some random high anomaly score claims (anomalies without specific flags) - 2% of claims
        if random.random() < 0.02 and not has_fraud_flag:
            base_risk += random.uniform(60, 80)
            anomaly_scores[i] = random.uniform(0.8, 1.0)
            
        risk_scores[i] = min(max(base_risk, 0), 100)
        
    risk_categories = []
    for score in risk_scores:
        if score <= 30:
            risk_categories.append('Low')
        elif score <= 60:
            risk_categories.append('Medium')
        elif score <= 80:
            risk_categories.append('High')
        else:
            risk_categories.append('Critical')
            
    # Build dataframe
    df = pd.DataFrame({
        'claim_id': claim_ids,
        'hospital_id': hospital_assignments,
        'state': state_assignments,
        'procedure_code': procedure_assignments,
        'claim_amount': claim_amounts,
        'anomaly_score': np.round(anomaly_scores, 4),
        'image_reuse_flag': image_reuse_flag,
        'duplicate_flag': duplicate_flag,
        'risk_score': np.round(risk_scores, 2),
        'risk_category': risk_categories
    })
    
    return df

if __name__ == "__main__":
    df = load_mock_data()
    print(df.head())
    print("\nRisk Category Distribution:")
    print(df['risk_category'].value_counts())
    print("\nTotal Claims:", len(df))

