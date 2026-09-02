def detect_voice_risk(ai_probability):

    risk_score = ai_probability

    if risk_score < 30:
        result = "LOW RISK"
        action = "ALLOW CALL"

    elif risk_score < 70:
        result = "MEDIUM RISK"
        action = "VERIFY CALLER"

    else:
        result = "HIGH RISK"
        action = "BLOCK AND ALERT"

    return {
        "risk_score": risk_score,
        "result": result,
        "recommended_action": action
    }