def generate_audit_summary(hospital_id, hospital_stats):
    """
    Generates a structured explanation paragraph for high-risk hospitals.
    No external API calls are made here.
    """
    duplicate_count = hospital_stats.get('duplicate_count', 0)
    image_reuse_count = hospital_stats.get('image_reuse_count', 0)
    percentage = round(hospital_stats.get('avg_claim_deviation', 0.0), 2)
    risk_category = hospital_stats.get('risk_category', 'Unknown')
    
    summary = (
        f"Hospital {hospital_id} exhibits elevated fraud indicators. "
        f"{duplicate_count} duplicate claims and {image_reuse_count} diagnostic image reuse cases were detected. "
        f"Average claim deviation is {percentage}%. "
        f"Composite risk score classified as {risk_category}. "
        "Recommended for secondary audit review."
    )
    
    return summary
