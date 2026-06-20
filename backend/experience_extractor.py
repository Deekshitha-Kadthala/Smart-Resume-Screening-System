import re


# -----------------------------------
# EXTRACT EXPERIENCE
# -----------------------------------

def extract_experience(text):

    text = text.lower()

    patterns = [

        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*year',
        r'(\d+)\+?\s*yrs',
        r'(\d+)\+?\s*yr'

    ]

    experience_years = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            try:
                experience_years.append(
                    int(match)
                )

            except:
                pass

    if len(experience_years) == 0:
        return 0

    return max(experience_years)


# -----------------------------------
# EXPERIENCE SCORE
# -----------------------------------

def calculate_experience_score(
        years
):

    if years >= 10:
        return 100

    elif years >= 8:
        return 90

    elif years >= 6:
        return 80

    elif years >= 4:
        return 70

    elif years >= 2:
        return 60

    elif years >= 1:
        return 50

    else:
        return 20


# -----------------------------------
# EXPERIENCE ANALYSIS
# -----------------------------------

def analyze_experience(text):

    years = extract_experience(
        text
    )

    score = calculate_experience_score(
        years
    )

    return {

        "years": years,

        "experience_score": score

    }


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    sample_text = """
    Software Engineer with
    4 years experience in Python,
    Flask and SQL.
    """

    result = analyze_experience(
        sample_text
    )

    print(result)