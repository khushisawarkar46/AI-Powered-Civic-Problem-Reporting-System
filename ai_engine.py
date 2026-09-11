import re


def detect_language(text):
    """
    Simple language detection without external libraries.
    """

    if re.search(r"[\u0900-\u097F]", text):
        return "Marathi/Hindi"

    english_words = [
        "the", "is", "there", "water", "road",
        "waste", "garbage", "street", "problem",
        "leakage", "pothole"
    ]

    words = text.lower().split()

    count = 0

    for word in words:
        if word in english_words:
            count += 1

    if count > 0:
        return "English"

    return "Unknown"


def classify_problem(text):

    text = text.lower()

    # Pothole / Road
    if any(word in text for word in [
        "pothole",
        "road damage",
        "broken road",
        "road damaged",
        "road problem",
        "खड्डा",
        "रस्ता"
    ]):

        return (
            "Pothole / Road Damage",
            "Public Works Department"
        )

    # Street Problem
    if any(word in text for word in [
        "street light",
        "streetlight",
        "street lamp",
        "light not working",
        "lamp not working",
        "रस्त्याचा दिवा",
        "स्ट्रीट लाईट"
    ]):

        return (
            "Street Problem",
            "Street Light Department"
        )

    # Water Leakage
    if any(word in text for word in [
        "water leakage",
        "water leak",
        "pipe leakage",
        "pipe leak",
        "leaking pipe",
        "गळती",
        "पाण्याची गळती"
    ]):

        return (
            "Water Leakage",
            "Water Supply Department"
        )

    # Waste / Garbage
    if any(word in text for word in [
        "garbage",
        "waste",
        "dustbin",
        "trash",
        "dirty area",
        "kachra",
        "कचरा",
        "घाण"
    ]):

        return (
            "Waste / Garbage",
            "Waste Management Department"
        )

    # Drainage / Sewage
    if any(word in text for word in [
        "drainage",
        "drain",
        "sewage",
        "sewer",
        "blocked drain",
        "नाली",
        "गटार"
    ]):

        return (
            "Drainage / Sewage",
            "Drainage Department"
        )

    # Water Supply
    if any(word in text for word in [
        "no water",
        "water supply",
        "water shortage",
        "water not coming",
        "पाणी येत नाही",
        "पाणीपुरवठा"
    ]):

        return (
            "Water Supply",
            "Water Supply Department"
        )

    # Electricity
    if any(word in text for word in [
        "electricity",
        "electric",
        "power cut",
        "power failure",
        "electric pole",
        "wire problem",
        "वीज",
        "लाईट"
    ]):

        return (
            "Electricity Problem",
            "Electricity Department"
        )

    return (
        "Other",
        "Municipal Corporation"
    )


def predict_priority(text):

    text = text.lower()

    high_words = [
        "danger",
        "dangerous",
        "accident",
        "injury",
        "fire",
        "electric shock",
        "overflow",
        "major leakage",
        "emergency",
        "धोका",
        "अपघात",
        "आग"
    ]

    medium_words = [
        "large",
        "big",
        "serious",
        "blocked",
        "broken",
        "leakage",
        "garbage",
        "damage"
    ]

    for word in high_words:

        if word in text:
            return "High"

    for word in medium_words:

        if word in text:
            return "Medium"

    return "Low"


def calculate_confidence(category, text):

    text = text.lower()

    keywords = {

        "Pothole / Road Damage": [
            "pothole",
            "road",
            "खड्डा",
            "रस्ता"
        ],

        "Street Problem": [
            "street",
            "streetlight",
            "lamp",
            "light"
        ],

        "Water Leakage": [
            "leak",
            "leakage",
            "pipe",
            "गळती"
        ],

        "Waste / Garbage": [
            "garbage",
            "waste",
            "trash",
            "kachra",
            "कचरा"
        ],

        "Drainage / Sewage": [
            "drain",
            "drainage",
            "sewage",
            "sewer",
            "गटार"
        ],

        "Water Supply": [
            "water supply",
            "no water",
            "water shortage",
            "पाणी"
        ],

        "Electricity Problem": [
            "electricity",
            "electric",
            "power",
            "वीज"
        ]
    }

    if category not in keywords:
        return 0.60

    found = 0

    for word in keywords[category]:

        if word in text:
            found += 1

    if found >= 2:
        return 0.95

    if found == 1:
        return 0.85

    return 0.70


def generate_report(
    category,
    priority,
    department,
    language,
    confidence
):

    report = (
        "AI analyzed the citizen complaint. "
        "The detected civic problem is "
        f"{category}. "
        f"The predicted priority is {priority}. "
        f"The recommended department is {department}. "
        f"Detected language: {language}. "
        f"AI confidence is {confidence * 100:.0f}%. "
        "The complaint has been forwarded for officer review."
    )

    return report


def analyze_complaint(text):

    if not text or not text.strip():

        return {
            "category": "Other",
            "priority": "Low",
            "department": "Municipal Corporation",
            "language": "Unknown",
            "confidence": 0.0,
            "report": "No complaint description provided."
        }

    # 1. Detect language
    language = detect_language(text)

    # 2. Classify civic problem
    category, department = classify_problem(text)

    # 3. Predict priority
    priority = predict_priority(text)

    # 4. Calculate confidence
    confidence = calculate_confidence(
        category,
        text
    )

    # 5. Generate AI report
    report = generate_report(
        category,
        priority,
        department,
        language,
        confidence
    )

    return {
        "category": category,
        "priority": priority,
        "department": department,
        "language": language,
        "confidence": confidence,
        "report": report
    }