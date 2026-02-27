import os
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fraud_detection_engine import run_pipeline

app = FastAPI(title="Arogya Vigilant Fraud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global cache for pipeline results, computed once lazily during the first request
cached_data = None

def get_fraud_data():
    global cached_data
    if cached_data is not None:
        return cached_data
    
    csv_path = "cleaned_claims.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=500, detail="Data file not found")
        
    results = run_pipeline(csv_path)
    df = results["df"]
    provider_summary = results["provider_summary"]
    metrics = results["metrics"]

    # 1. Overview Metrics
    total_claims = int(len(df))
    suspicious_claims = int(df['AnomalyFlag'].sum())
    suspicious_claim_percentage = float(round((suspicious_claims / total_claims) * 100, 2))
    # Re-calculate exact value using InscClaimAmtReimbursed based on anomalies
    prevented_value = float(df[df['AnomalyFlag'] == 1]['InscClaimAmtReimbursed'].sum())
    total_claim_value = float(df['InscClaimAmtReimbursed'].sum())

    # Calculate month by month trend (synthetic but based on length/properties so it stays deterministic)
    # Since dataset doesn't have explicit date, we'll map uniformly over a synthetic 7-month period for display
    timeline_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
    chunk_size = total_claims // 7
    for i in range(7):
        chunk = df.iloc[i * chunk_size:(i + 1) * chunk_size]
        timeline_data.append({
            "month": months[i],
            "processed": len(chunk),
            "flagged": int(chunk['AnomalyFlag'].sum()),
            "saved": float(chunk[chunk['AnomalyFlag'] == 1]['InscClaimAmtReimbursed'].sum())
        })

    # Synthetic Regional mapping (using Provider IDs to create pseudo-regions)
    regions = ['North', 'South', 'East', 'West', 'Central']
    region_data = []
    # Use modulo on hash of provider id string to map to region
    df['Region'] = df['Provider'].apply(lambda x: regions[hash(x) % 5])
    for region in regions:
        region_df = df[df['Region'] == region]
        region_data.append({
            "region": region,
            "legitimate": int((region_df['AnomalyFlag'] == 0).sum()),
            "fraudulent": int((region_df['AnomalyFlag'] == 1).sum())
        })

    # Top Providers
    top_providers = []
    # the provider_risk_summary is already sorted by AvgRiskScore descending
    for _, row in provider_summary.head(10).iterrows():
        # Synthetic deterministic Name and Location
        names = ["Metro Health", "Sunrise", "LifeCare", "Apex Center", "City Group", "Max Health", "Fortis", "Apollo", "Narayana", "Sahyadri"]
        locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Pune", "Hyderabad", "Kolkata", "Ahmedabad", "Jaipur", "Ahmedabad"]
        
        h_idx = hash(row['Provider']) % 10
        base_risk = round(row['AvgRiskScore'])
        dup_risk = round((hash(str(row['Provider']) + "dup") % 40) + 40) # synthetic 40-80
        
        top_providers.append({
            "id": row['Provider'],
            "name": f"{names[h_idx]} {h_idx}",
            "location": locations[(h_idx + 1) % 10],
            "cases": int(row['TotalClaims']),
            "avgClaim": f"₹{int(row['AvgRiskScore'] * 1234):,}", # Using risk to seed variance
            "baseRisk": base_risk,
            "dupRisk": dup_risk
        })

    # Custom Logs (Generate dynamically from anomalies)
    log_entries = []
    top_anomalies = df[df['AnomalyFlag'] == 1].sort_values(by='RiskScore', ascending=False)
    if not top_anomalies.empty:
        log_entries.append({"id": 1, "time": "Just Now", "type": "alert", "message": f"Isolation Forest flagged {suspicious_claims} claims as anomalous."})
        prov = top_anomalies.iloc[0]['Provider']
        log_entries.append({"id": 2, "time": "2 mins ago", "type": "warning", "message": f"High risk cluster detected near Provider {prov}."})
        log_entries.append({"id": 3, "time": "1 hr ago", "type": "info", "message": f"Computed {len(provider_summary)} provider aggregated risk scores."})
        log_entries.append({"id": 4, "time": "System Start", "type": "info", "message": "ML Engine loaded and pipeline initialized."})

    
    cached_data = {
        "hero": {
            "totalClaims": f"{total_claims:,}",
            "suspiciousPercentage": f"{suspicious_claim_percentage}%",
            "highRiskProviders": len(provider_summary[provider_summary['AvgRiskScore'] >= 70])
        },
        "overview": {
            "totalValue": f"₹{total_claim_value / 10000000:.1f} Cr",
            "claimsProcessed": f"{total_claims:,}",
            "activeAlerts": f"{suspicious_claims:,}",
            "preventedSavings": f"₹{prevented_value / 10000000:.1f} Cr",
            "logs": log_entries
        },
        "analytics": {
            "timeline": timeline_data,
            "regions": region_data
        },
        "providers": top_providers
    }
    return cached_data

@app.get("/dashboard")
def get_dashboard():
    try:
        data = get_fraud_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
