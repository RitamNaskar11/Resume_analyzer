from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from src.resume_parser import extract_text_from_pdf, extract_skills
from src.job_matcher import extract_job_skills
from src.scoring import calculate_score
from src.ai_analyzer import analyze_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
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

    # 5. Resume ke skills nikalo
    resume_skills = extract_skills(resume_text)

    # 6. Job description se required skills nikalo
    job_skills = extract_job_skills(job_description)

    # 7. Score calculate karo 
    score, matched_skills, missing_skills = calculate_score(resume_skills, job_skills)

# 8. AI analysis
    ai_result = analyze_resume(resume_text)

    return render_template(
        "index.html",
        resume_skills=resume_skills,
        job_skills=job_skills,
        score = score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        ai_result=ai_result
)


if __name__ == "__main__":
    app.run(debug=True)


# print("Resume Skills:", resume_skills)
# print("Job Skills:", job_skills)
# print("Matched Skills:", matched_skills)
# print("Missing Skills:", missing_skills)
# print("Score:", score)
# print(ai_result)
