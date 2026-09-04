from src.resume_parser import extract_text_from_pdf, extract_skills
from src.job_matcher import extract_job_skills
from src.scoring import calculate_score

pdf_path = "data/resume.pdf"

resume_text = extract_text_from_pdf(pdf_path)
resume_skills = extract_skills(resume_text)
print("Resume Skills:",resume_skills)


job_description = """We are looking for a skilled Python developer with experience
in AWS, SQL, and JavaScript. Knowledge of HTML, CSS, and Bootstrap is a plus.
"""

job_skills=extract_job_skills(job_description)

score , missing_skills, matched_skills = calculate_score (resume_skills,job_skills)

print("Job Skills:",job_skills)
print("Matched Skills:",matched_skills)
print("Missing Skills:",missing_skills)
print("Score:",score)
