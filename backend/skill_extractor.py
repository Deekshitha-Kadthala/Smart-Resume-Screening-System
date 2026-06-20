import re

# Master Skill Database

SKILLS_DATABASE = [

    # Programming

    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",

    # Web

    "html",
    "css",
    "bootstrap",
    "react",
    "angular",
    "vue",
    "nodejs",
    "express",

    # Databases

    "mysql",
    "sql",
    "sqlite",
    "postgresql",
    "mongodb",

    # Data Science

    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "power bi",
    "tableau",

    # AI / ML

    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",

    # Cloud

    "aws",
    "azure",
    "gcp",

    # Tools

    "git",
    "github",
    "docker",
    "linux",

    # Frameworks

    "flask",
    "django",
    "spring",
    "hibernate",

    # Others

    "data structures",
    "algorithms",
    "oop",
    "rest api",
    "microservices"
]


# ----------------------------------
# CLEAN TEXT
# ----------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)

    return text


# ----------------------------------
# EXTRACT SKILLS
# ----------------------------------

def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS_DATABASE:

        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# ----------------------------------
# SKILL MATCH
# ----------------------------------

def skill_match(resume_skills, jd_skills):

    matched = []

    for skill in resume_skills:

        if skill in jd_skills:
            matched.append(skill)

    return matched


# ----------------------------------
# MISSING SKILLS
# ----------------------------------

def missing_skills(resume_skills, jd_skills):

    missing = []

    for skill in jd_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing


# ----------------------------------
# SKILL SCORE
# ----------------------------------

def calculate_skill_score(
        resume_skills,
        jd_skills
):

    if len(jd_skills) == 0:
        return 0

    matched = skill_match(
        resume_skills,
        jd_skills
    )

    score = (
        len(matched)
        /
        len(jd_skills)
    ) * 100

    return round(score, 2)


# ----------------------------------
# COMPLETE ANALYSIS
# ----------------------------------

def analyze_skills(
        resume_text,
        jd_text
):

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        jd_text
    )

    matched = skill_match(
        resume_skills,
        jd_skills
    )

    missing = missing_skills(
        resume_skills,
        jd_skills
    )

    score = calculate_skill_score(
        resume_skills,
        jd_skills
    )

    return {

        "resume_skills": resume_skills,

        "jd_skills": jd_skills,

        "matched_skills": matched,

        "missing_skills": missing,

        "skill_score": score

    }


# ----------------------------------
# TESTING
# ----------------------------------

if __name__ == "__main__":

    resume = """
    Python
    Flask
    SQL
    Machine Learning
    Git
    """

    jd = """
    Python
    Flask
    Machine Learning
    Docker
    AWS
    """

    result = analyze_skills(
        resume,
        jd
    )

    print(result)