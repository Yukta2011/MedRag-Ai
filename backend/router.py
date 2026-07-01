import re


def route_question(question):
    """Route question to local or cloud LLM based on content"""
    question_lower = question.lower()

    # PHI / sensitive data patterns
    phi_patterns = [
        r'\bpatient\b',
        r'\bname\b',
        r'\bssn\b',
        r'\bdate of birth\b',
        r'\bmedical record\b',
        r'\bdiagnosis\b.*\bpatient\b',
        r'\bdr\.\s+\w+',
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # DOB
    ]

    for pattern in phi_patterns:
        if re.search(pattern, question_lower):
            return "local"

    # General medical research questions go to cloud
    return "cloud"


if __name__ == "__main__":
    print(router_question("What is diabetes?"))  # cloud
    print(router_question("Patient John Doe has diabetes symptoms"))  # local