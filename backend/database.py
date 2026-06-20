import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "../database/resumes.db"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "..", "database", "resumes.db")
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def get_connection():

    conn = sqlite3.connect(
        DATABASE,
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn

# -----------------------------
# CREATE TABLES
# -----------------------------

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Recruiters / Admins

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Job Descriptions

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        job_description TEXT,
        created_at TEXT
    )
    """)

    # Resume Records

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        email TEXT,
        phone TEXT,

        skills TEXT,
        education TEXT,

        experience INTEGER,

        ats_score REAL,
        match_score REAL,

        final_score REAL,
        rank_position INTEGER,

        resume_file TEXT,

        uploaded_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# USER MANAGEMENT
# -----------------------------

def add_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(username,password)
    VALUES(?,?)
    """, (username, password))

    conn.commit()
    conn.close()


def get_user(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user

# -----------------------------
# ADD USER
# -----------------------------


def add_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = generate_password_hash(password)

    cursor.execute("""
    INSERT INTO users(username,password)
    VALUES(?,?)
    """, (username, hashed_pw))

    conn.commit()
    conn.close()

# -----------------------------
# JOB MANAGEMENT
# -----------------------------

def add_job(job_title, job_description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jobs(
    job_title,
    job_description,
    created_at
    )
    VALUES(?,?,?)
    """,
                   (
                       job_title,
                       job_description,
                       datetime.now().strftime(
                           "%Y-%m-%d %H:%M:%S"
                       )
                   ))

    conn.commit()
    conn.close()


def get_all_jobs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM jobs
    ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def get_job(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM jobs
    WHERE id=?
    """, (job_id,))

    job = cursor.fetchone()

    conn.close()

    return job


# -----------------------------
# RESUME INSERT
# -----------------------------

def insert_resume(
        name,
        email,
        phone,
        skills,
        education,
        experience,
        ats_score,
        match_score,
        final_score,
        rank_position,
        resume_file
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO resumes(

    name,
    email,
    phone,

    skills,
    education,

    experience,

    ats_score,
    match_score,

    final_score,
    rank_position,

    resume_file,

    uploaded_at

    )

    VALUES(
    ?,?,?,?,?,?,?,?,?,?,?,?
    )
    """,

                   (
                       name,
                       email,
                       phone,
                       skills,
                       education,
                       experience,
                       ats_score,
                       match_score,
                       final_score,
                       rank_position,
                       resume_file,
                       datetime.now().strftime(
                           "%Y-%m-%d %H:%M:%S"
                       )
                   ))

    conn.commit()
    conn.close()


# -----------------------------
# FETCH ALL RESUMES
# -----------------------------

def get_all_resumes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resumes
    ORDER BY final_score DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# FETCH SINGLE RESUME
# -----------------------------

def get_resume_by_id(resume_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resumes
    WHERE id=?
    """, (resume_id,))

    data = cursor.fetchone()

    conn.close()

    return data


# -----------------------------
# DELETE RESUME
# -----------------------------

def delete_resume(resume_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM resumes
    WHERE id=?
    """, (resume_id,))

    conn.commit()
    conn.close()


# -----------------------------
# SEARCH CANDIDATES
# -----------------------------

def search_candidate(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resumes
    WHERE name LIKE ?
    OR email LIKE ?
    OR skills LIKE ?
    """,

                   (
                       "%" + keyword + "%",
                       "%" + keyword + "%",
                       "%" + keyword + "%"
                   ))

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# TOP CANDIDATES
# -----------------------------

def get_top_candidates(limit=10):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resumes
    ORDER BY final_score DESC
    LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# DASHBOARD STATS
# -----------------------------

def total_resumes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM resumes
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def average_score():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(final_score)
    FROM resumes
    """)

    avg = cursor.fetchone()[0]

    conn.close()

    return round(avg, 2) if avg else 0


def top_candidate():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resumes
    ORDER BY final_score DESC
    LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    return data

def total_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

# -----------------------------
# INITIALIZATION
# -----------------------------

if __name__ == "__main__":

    create_tables()

    print("Database Created Successfully")

    from werkzeug.security import check_password_hash

def check_login(username, password):

    user = get_user(username)

    if user and check_password_hash(
        user["password"],
        password
    ):
        return user

    return None