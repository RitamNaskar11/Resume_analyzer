from flask import (
    Flask, render_template, request,redirect, url_for, session,
send_from_directory, flash
)

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from src.resume_parser import extract_text_from_pdf, extract_skills
from src.job_matcher import extract_job_skills
from src.scoring import calculate_score
from src.ai_analyzer import analyze_resume

from models import db, User
import os

from functools import wraps





app = Flask(__name__)

def login_required(route_function):
    @wraps(route_function)

    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    return wrapper

app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-secret-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", ""
).replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# signup page function
@app.route("/signup", methods = ["GET" , "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        confirm_password = request.form.get("confirm_password","")

        if not name or not email or not password:
            flash("All field are required.", "error")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Password do not match", "error")
            return redirect(url_for("signup"))

        if len(password)<8:
            flash("Password must contain at least 8 characters", "error")
            return redirect(url_for("signup"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email alrady registered please login", "error")
            return redirect(url_for("signup"))

        hash_password = generate_password_hash(password)

        new_user = User (
            name = name,
            email=email,
            password = hash_password
        )

        db.session.add (new_user)
        db.session.commit()

        flash("Account crated successfully! please login your account" , "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# login page function
@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash (user.password, password):
            
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("analyzer"))
        
        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

# logout function 
@app.route("/logout")
def logout():
    session.clear()

    flash("You have been loged out","success")
    return redirect(url_for("landing"))

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/analyzer")
@login_required
def analyzer():
    return render_template("analyzer.html")

@app.route("/results")
@login_required
def results():
    analysis = session.pop("analysis", None)

    if analysis:
        return render_template(
            "index.html",
            resume_skills=analysis["resume_skills"],
            job_skills=analysis["job_skills"],
            score=analysis["score"],
            matched_skills=analysis["matched_skills"],
            missing_skills=analysis["missing_skills"],
            ai_result=analysis["ai_result"],
            uploaded_filename=analysis["uploaded_filename"]

        )
    return render_template("index.html")



@app.route("/uploads/<filename>")
@login_required
def upload_file(filename):
    return send_from_directory("uploads",filename)
    

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
    # 1. Resume receive karo
    resume = request.files["resume"]

    # 2. Job description receive karo
    job_description = request.form["job_description"]

    filename = secure_filename(resume.filename)
    pdf_path = os.path.join("uploads", filename)
    resume.save(pdf_path)

    # 4. Resume se text extract karo
    resume_text = extract_text_from_pdf(pdf_path)
    print(resume_text)

    # 5. Resume ke skills nikalo
    resume_skills = extract_skills(resume_text)

    # 6. Job description se required skills nikalo
    job_skills = extract_job_skills(job_description)

    # 7. Score calculate karo
    score, matched_skills, missing_skills = calculate_score(resume_skills, job_skills)

    # 8. AI analysis
    ai_result = analyze_resume(
        resume_text, job_description, matched_skills, missing_skills
    )
    session ["analysis"] = {
    "resume_skills": resume_skills,
    "job_skills": job_skills,
    "score": score,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "ai_result": ai_result,
    "uploaded_filename": filename
    }
    return redirect(url_for("results"))


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        print("PostgreSQL database connected successfully!")
    app.run(debug=True)


