from difflib import SequenceMatcher

def similarity(a, b):
    if not a or not b:
        return 0
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)

def verify_data(extracted_fields, user_input):
    results = {}

    for field, user_value in user_input.items():
        extracted_value = extracted_fields.get(field, "")

        score = similarity(
            str(extracted_value).lower(),
            str(user_value).lower()
        )

        results[field] = {
            "extracted": extracted_value,
            "entered": user_value,
            "match": score >= 80,
            "confidence": score
        }

    return results
