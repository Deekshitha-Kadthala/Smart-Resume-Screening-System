from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# ----------------------------------
# CLEAN TEXT
# ----------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9\s]',
        ' ',
        text
    )

    return text


# ----------------------------------
# TF-IDF MATCHING
# ----------------------------------

def calculate_similarity(resume_text, jd_text):

    if not resume_text or not jd_text:
        return 0

    try:

        resume_text = clean_text(str(resume_text))
        jd_text = clean_text(str(jd_text))

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf_matrix = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    except Exception as e:

        print("Matcher Error:", str(e))
        return 0

# ----------------------------------
# KEYWORD MATCH
# ----------------------------------

def keyword_match_score(
        resume_text,
        jd_text
):

    resume_words = set(
        clean_text(
            resume_text
        ).split()
    )

    jd_words = set(
        clean_text(
            jd_text
        ).split()
    )

    if len(jd_words) == 0:
        return 0

    matched = resume_words.intersection(
        jd_words
    )

    score = (
        len(matched)
        /
        len(jd_words)
    ) * 100

    return round(score, 2)


# ----------------------------------
# COMPLETE MATCH ANALYSIS
# ----------------------------------

def analyze_match(resume_text, jd_text):

    try:

        similarity_score = calculate_similarity(
            resume_text,
            jd_text
        )

        keyword_score = keyword_match_score(
            resume_text,
            jd_text
        )

    except Exception as e:

        print("Analyze Match Error:", e)

        similarity_score = 0
        keyword_score = 0

    return {
        "similarity_score": similarity_score,
        "keyword_score": keyword_score
    }

# ----------------------------------
# TEST
# ----------------------------------

if __name__ == "__main__":

    resume = """
    Python Developer
    Flask
    Machine Learning
    SQL
    """

    jd = """
    Looking for Python Developer
    with Flask and SQL knowledge
    """

    result = analyze_match(
        resume,
        jd
    )

    print(result)