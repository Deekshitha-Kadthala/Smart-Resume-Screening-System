import re

EDUCATION_KEYWORDS = [

    "b.tech",
    "btech",
    "b.e",
    "be",

    "m.tech",
    "mtech",

    "mba",

    "bca",
    "mca",

    "bsc",
    "msc",

    "phd",

    "intermediate",
    "ssc",
    "10th",
    "12th"
]


def extract_education(text):

    text = text.lower()

    found = []

    for degree in EDUCATION_KEYWORDS:

       if re.search(r'\b' + re.escape(degree) + r'\b', text):
            found.append(degree.upper())

    return list(set(found))


def education_score(
        education_list
):

    score = 0

    if "B.TECH" in education_list:
        score += 40

    if "M.TECH" in education_list:
        score += 20

    if "MBA" in education_list:
        score += 15

    if "MCA" in education_list:
        score += 15

    if "PHD" in education_list:
        score += 25

    return min(score, 100)


if __name__ == "__main__":

    sample = """
    Completed B.Tech in CSE.
    Pursuing M.Tech.
    """

    print(
        extract_education(sample)
    )