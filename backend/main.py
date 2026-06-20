from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
from werkzeug.security import check_password_hash
from flask import flash
from export_excel import export_to_excel
from database import add_job, get_all_jobs
from database import total_jobs



from database import (
    create_tables,
    insert_resume,
    get_all_resumes,
    get_resume_by_id,
    delete_resume,
    search_candidate,
    add_user,
    get_user,
    total_resumes,
    total_jobs,
    average_score,
    get_top_candidates
)

from resume_parser import parse_resume
from matcher import analyze_match
from skill_extractor import analyze_skills
from experience_extractor import analyze_experience
from ats_score import generate_ats_result
from report_generator import generate_candidate_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "templates"),
    static_folder=os.path.join(BASE_DIR, "..", "static")
)

app.secret_key = "smart_resume_secret_123"

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "static",
    "uploads"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "reports"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------------------
# INIT DATABASE
# -------------------------------
create_tables()


# -------------------------------
# HOME PAGE
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ===============================
# AUTH ROUTES
# ===============================

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = get_user(username)

        if existing_user:
            flash("Username already exists")
            return redirect("/register")

        add_user(username, password)

        flash("Registration Successful. Please Login.")
        return redirect("/login")

    return render_template("register.html")

#LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user and check_password_hash(
                user["password"],
                password
        ):
            session["user"] = username
            return redirect("/dashboard")

        flash("Invalid Username or Password")

    return render_template("login.html")
    
# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# ===============================
# DASHBOARD
# ===============================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    total = total_resumes()

    avg = average_score()

    candidates = get_top_candidates(5)

    top_score = 0
    top_candidate_name = "No Candidate"

    if len(candidates) > 0:

        top_score = candidates[0]["final_score"]

        top_candidate_name = candidates[0]["name"]

    return render_template(
        "dashboard.html",

        total=total,

        avg=avg,

        top_score=top_score,

        top_candidate_name=top_candidate_name,

        candidates=candidates
    )
# -------------------------------
# UPLOAD RESUMES
# -------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        jd_text = request.form.get("jd", "").strip()

        files = request.files.getlist("resume")

        candidates = []

        for file in files:

            # Skip empty selection
            if file.filename == "":
                continue

            # Allow only PDF files
            if not file.filename.lower().endswith(".pdf"):
                flash(f"{file.filename} is not a PDF")
                continue

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(file_path)

            parsed = parse_resume(file_path)

            if not parsed:
                flash("Resume parsing failed")
                continue

            resume_text = parsed.get("resume_text", "")

            if not resume_text or resume_text.strip() == "":
                flash(f"No text found in {file.filename}")
                continue

            skill_data = analyze_skills(
                resume_text,
                jd_text
            )

            exp_data = analyze_experience(
                resume_text
            )

            match_data = analyze_match(
                resume_text,
                jd_text
            )

            ats = generate_ats_result(
                skill_data["skill_score"],
                exp_data["experience_score"],
                parsed["education"],
                match_data["similarity_score"]
            )

            candidate = {
                 "name": parsed["name"],

                "email": parsed["email"],

                "phone": parsed["phone"],

                "skills": skill_data["resume_skills"],

                "education": parsed["education"],

                "experience": parsed["experience"],

                "skill_score": ats["skill_score"],

                "similarity_score": ats["similarity_score"],

                "final_score": ats["final_score"],

                "file": file.filename
            }

            candidates.append(candidate)

        candidates.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        rank = 1

        for c in candidates:

            c["rank_position"] = rank

            insert_resume(
                   c["name"],
                c["email"],
                c["phone"],
                ",".join(c["skills"]),
                str(c["education"]),
                c["experience"],
                c["skill_score"],
                c["similarity_score"],
                c["final_score"],
                c["rank_position"],
                c["file"]
            )

            rank += 1

        return render_template(
            "result.html",
            candidates=candidates
        )

    return render_template("upload.html")

# -------------------------------
# RECORDS PAGE
# -------------------------------
@app.route("/records")
def records():

    if "user" not in session:
        return redirect("/login")

    data = get_all_resumes()

    return render_template("records.html", records=data)


# -------------------------------
# SEARCH
# -------------------------------
@app.route("/search", methods=["GET", "POST"])
def search():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        keyword = request.form.get("keyword", "")

        data = search_candidate(keyword)

    else:
        data = get_all_resumes()

    return render_template(
        "records.html",
        records=data
    )

# -------------------------------
# DELETE RECORD
# -------------------------------
@app.route("/delete/<int:id>")
def delete(id):

    if "user" not in session:
        return redirect("/login")

    delete_resume(id)

    return redirect(url_for("records"))


# -------------------------------
# PDF REPORT
# -------------------------------
@app.route("/report/<int:id>")
def report(id):

    if "user" not in session:
        return redirect("/login")

    data = get_resume_by_id(id)

    if not data:
        return "Record not found"

    candidate = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "skills": data["skills"].split(","),
        "education": data["education"],
        "experience": data["experience"],
        "skill_score": data["ats_score"],
        "experience_score": 0,
        "education_score": 0,
        "similarity_score": data["match_score"],
        "final_score": data["final_score"],
        "rank_position": data["rank_position"]
    }

    pdf_path = generate_candidate_report(candidate)

    return send_file(pdf_path, as_attachment=True)

@app.route("/download_excel")
def download_excel():

    if "user" not in session:
        return redirect("/login")

    file_path = export_to_excel()

    return send_file(file_path, as_attachment=True)

@app.route("/job", methods=["GET"])
def job_page():

    if "user" not in session:
        return redirect("/login")

    return render_template("job.html")


@app.route("/add_job", methods=["GET", "POST"])
def add_job_route():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        desc = request.form["description"]

        add_job(title, desc)

        return redirect("/job")

    return render_template("job.html")

# -------------------------------
# COMPARE ROUTE
# -------------------------------

@app.route("/compare", methods=["GET", "POST"])
def compare():

    if "user" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":

        try:
            id1 = int(request.form.get("id1", 0))
        except (ValueError, TypeError):
            id1 = 0

        try:
            id2 = int(request.form.get("id2", 0))
        except (ValueError, TypeError):
            id2 = 0

        c1 = get_resume_by_id(id1)
        c2 = get_resume_by_id(id2)

        result = {
            "c1": c1,
            "c2": c2
        }

    return render_template("compare.html", result=result)

# -------------------------------
# SKILL GAP ANALYSIS
# -------------------------------
@app.route("/skill_gap/<int:id>")
def skill_gap(id):

    if "user" not in session:
        return redirect("/login")

    data = get_resume_by_id(id)

    skills = data["skills"].split(",")

    common_skills = ["python", "java", "sql", "flask"]

    missing = [s for s in common_skills if s not in skills]

    return {
        "candidate": data["name"],
        "missing_skills": missing
    }

@app.route("/test")
def test():
    return "Flask Working"

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    app.run(debug=True)