import pdfplumber
import re

from skill_extractor import extract_skills
from education_extractor import extract_education
from experience_extractor import analyze_experience


# -----------------------------------
# PDF TEXT EXTRACTION
# -----------------------------------

import pdfplumber

def extract_text(pdf_path):

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        print("PDF Error:", str(e))
        return ""

    return text

# -----------------------------------
# NAME EXTRACTION
# -----------------------------------

def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 2:

            return line

    return "Unknown"


# -----------------------------------
# EMAIL EXTRACTION
# -----------------------------------

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group()

    return "Not Found"


# -----------------------------------
# PHONE EXTRACTION
# -----------------------------------

def extract_phone(text):

    pattern = r'(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}'

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group()

    return "Not Found"


# -----------------------------------
# COMPLETE PARSER
# -----------------------------------

def parse_resume(pdf_path):

    text = extract_text(pdf_path)

    if not text:
        return None

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    skills = extract_skills(text)
    education = extract_education(text)
    experience = analyze_experience(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience.get("years", 0),
        "experience_score": experience.get("experience_score", 0),
        "resume_text": text
    }

# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    path = "sample_resume.pdf"

    result = parse_resume(path)

    print(result)