import os
import pandas as pd
from database import get_all_resumes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "reports"
)

os.makedirs(REPORT_FOLDER, exist_ok=True)

def export_to_excel():

    data = get_all_resumes()

    rows = []

    for r in data:

        rows.append({
            "Name": r["name"],
            "Email": r["email"],
            "Phone": r["phone"],
            "Skills": r["skills"],
            "Experience": r["experience"],
            "ATS Score": r["final_score"],
            "Rank": r["rank_position"]
        })

    df = pd.DataFrame(rows)

    file_path = os.path.join(
        REPORT_FOLDER,
        "resume_report.xlsx"
    )

    df.to_excel(file_path, index=False)

    return file_path