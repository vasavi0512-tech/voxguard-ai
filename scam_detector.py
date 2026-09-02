def analyze_scam_text(text):

    text = text.lower()

    suspicious_words = [

        "otp",

        "password",

        "bank",

        "account",

        "pin",

        "urgent",

        "immediately",

        "send money",

        "transfer money",

        "transfer",

        "verification code",

        "share your details",

        "click this link",

        "pay now",

        "credit card",

        "debit card"

    ]


    score = 0

    detected_words = []


    for word in suspicious_words:

        if word in text:

            score += 10

            detected_words.append(
                word
            )


    if score > 100:

        score = 100


    if score >= 50:

        result = "HIGH SCAM RISK"

        action = (
            "STOP AND VERIFY THE CALLER"
        )


    elif score >= 20:

        result = "MEDIUM SCAM RISK"

        action = (
            "VERIFY THE CALLER BEFORE CONTINUING"
        )


    else:

        result = "LOW SCAM RISK"

        action = (
            "NO MAJOR SCAM INDICATORS DETECTED"
        )


    return {

        "risk_score":
            score,

        "result":
            result,

        "recommended_action":
            action,

        "suspicious_indicators":
            detected_words

    }