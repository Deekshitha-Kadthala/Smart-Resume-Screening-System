# ----------------------------------
# EDUCATION SCORE
# ----------------------------------

def calculate_education_score(
        education_list
):

    score = 0

    education_list = [
        item.upper()
        for item in education_list
    ]

    if "B.TECH" in education_list:
        score += 40

    if "B.E" in education_list:
        score += 40

    if "M.TECH" in education_list:
        score += 20

    if "MBA" in education_list:
        score += 15

    if "MCA" in education_list:
        score += 15

    if "MSC" in education_list:
        score += 15

    if "PHD" in education_list:
        score += 25

    return min(score, 100)


# ----------------------------------
# FINAL ATS SCORE
# ----------------------------------

def calculate_final_score(

        skill_score,

        experience_score,

        education_score,

        similarity_score

):

    final_score = (

        skill_score * 0.40 +

        experience_score * 0.25 +

        education_score * 0.20 +

        similarity_score * 0.15

    )

    return round(
        final_score,
        2
    )


# ----------------------------------
# COMPLETE ATS ANALYSIS
# ----------------------------------

def generate_ats_result(

        skill_score,

        experience_score,

        education_list,

        similarity_score

):

    education_score = (
        calculate_education_score(
            education_list
        )
    )

    final_score = (
        calculate_final_score(

            skill_score,

            experience_score,

            education_score,

            similarity_score

        )
    )

    return {

        "skill_score":
            skill_score,

        "experience_score":
            experience_score,

        "education_score":
            education_score,

        "similarity_score":
            similarity_score,

        "final_score":
            final_score

    }


# ----------------------------------
# TEST
# ----------------------------------

if __name__ == "__main__":

    result = generate_ats_result(

        skill_score=90,

        experience_score=80,

        education_list=[
            "B.TECH"
        ],

        similarity_score=85

    )

    print(result)