from src.resume_parser import extract_text_from_pdf, extract_skills
from src.job_matcher import extract_job_skills
from src.scoring import calculate_score

pdf_path = "data/resume.pdf"

resume_text = extract_text_from_pdf(pdf_path)
resume_skills = extract_skills(resume_text)
print("Resume Skills:",resume_skills)


