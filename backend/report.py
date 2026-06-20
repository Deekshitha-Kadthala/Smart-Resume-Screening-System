from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_pdf(data, output_path):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Resume Screening Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Name: {data['name']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Email: {data['email']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Phone: {data['phone']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Skills: {data['skills']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Score: {data['score']} %",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Rank: {data['rank']}",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return output_path