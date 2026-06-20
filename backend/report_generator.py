from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors

from datetime import datetime

import os


# ------------------------------------
# CREATE REPORT DIRECTORY
# ------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "reports"
)

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


# ------------------------------------
# GENERATE PDF REPORT
# ------------------------------------

def generate_candidate_report(candidate):

    filename = (
        candidate["name"]
        .replace(" ", "_")
        + "_Report.pdf"
    )

    filepath = os.path.join(
        REPORT_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    content = []

    # --------------------------------
    # TITLE
    # --------------------------------

    title = Paragraph(
        "AI Powered Resume Screening Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    # --------------------------------
    # DATE
    # --------------------------------

    content.append(

        Paragraph(
            f"Generated On : {datetime.now()}",
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 15)
    )

    # --------------------------------
    # CANDIDATE DETAILS
    # --------------------------------

    content.append(

        Paragraph(
            "<b>Candidate Information</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            f"Name : {candidate['name']}",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Email : {candidate['email']}",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Phone : {candidate['phone']}",
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 15)
    )

    # --------------------------------
    # EDUCATION
    # --------------------------------

    content.append(

        Paragraph(
            "<b>Education</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            str(candidate["education"]),
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 15)
    )

    # --------------------------------
    # EXPERIENCE
    # --------------------------------

    content.append(

        Paragraph(
            "<b>Experience</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            f"{candidate['experience']} Years",
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 15)
    )

    # --------------------------------
    # SKILLS
    # --------------------------------

    content.append(

        Paragraph(
            "<b>Skills</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            ", ".join(
                candidate["skills"]
            ),
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 15)
    )

    # --------------------------------
    # ATS ANALYSIS
    # --------------------------------

    content.append(

        Paragraph(
            "<b>ATS Analysis</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            f"Skill Score : "
            f"{candidate['skill_score']} %",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Experience Score : "
            f"{candidate['experience_score']} %",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Education Score : "
            f"{candidate['education_score']} %",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Similarity Score : "
            f"{candidate['similarity_score']} %",
            styles["Normal"]
        )

    )

    content.append(

        Paragraph(
            f"Final ATS Score : "
            f"{candidate['final_score']} %",
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 20)
    )

    # --------------------------------
    # RANKING
    # --------------------------------

    content.append(

        Paragraph(
            "<b>Candidate Ranking</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            f"Rank Position : "
            f"{candidate['rank_position']}",
            styles["Normal"]
        )

    )

    content.append(
        Spacer(1, 20)
    )

    # --------------------------------
    # RECOMMENDATION
    # --------------------------------

    recommendation = ""

    if candidate["final_score"] >= 85:

        recommendation = (
            "Highly Recommended"
        )

    elif candidate["final_score"] >= 70:

        recommendation = (
            "Recommended"
        )

    elif candidate["final_score"] >= 50:

        recommendation = (
            "Consider for Review"
        )

    else:

        recommendation = (
            "Not Recommended"
        )

    content.append(

        Paragraph(
            "<b>Recruiter Recommendation</b>",
            styles["Heading2"]
        )

    )

    content.append(

        Paragraph(
            recommendation,
            styles["Normal"]
        )

    )

    content.append(
        PageBreak()
    )

    # --------------------------------
    # BUILD PDF
    # --------------------------------

    doc.build(content)

    return filepath


# ------------------------------------
# TEST
# ------------------------------------

if __name__ == "__main__":

    sample_candidate = {

        "name": "John Doe",

        "email": "john@gmail.com",

        "phone": "9876543210",

        "education": ["B.TECH"],

        "experience": 3,

        "skills": [
            "Python",
            "Flask",
            "SQL"
        ],

        "skill_score": 90,

        "experience_score": 70,

        "education_score": 40,

        "similarity_score": 88,

        "final_score": 82,

        "rank_position": 1

    }

    path = generate_candidate_report(
        sample_candidate
    )

    print(
        "PDF Generated:",
        path
    )