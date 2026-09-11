import re
import PyPDF2

def extract_job_skills(job_description):
    skills = [
    "Python",
    "AWS",
    "SQL",
    "C++",
    "Django",
    "Go",
    "JavaScript",
    "Machine Learning",
    "Bootstrap",
    "GitHub",
    ]

    required_skills= []

    for skill in skills:
        pattern = r'(?<!\w)'+ re.escape (skill) +r'(?!\w)'
        if re.search(pattern, job_description ,re.IGNORECASE):
            required_skills.append(skill)

    return required_skills

job_description = "We are looking for a skilled Python developer with experience in AWS, SQL, and JavaScript. Knowledge of HTML, CSS, and Bootstrap is a plus."

# required_skills = extract_job_skills(job_description)
# print(required_skills)