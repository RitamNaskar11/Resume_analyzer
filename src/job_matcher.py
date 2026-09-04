def extract_job_skills(job_description):
    skills = [
    "Python",
    "AWS",
    "SQL",
    "C++",
    "Java",
    "Machine Learning",
    "Bootstrap",
    "GitHub",
    ]

    required_skills= []

    for skill in skills:
        if skill.lower() in job_description.lower():
            required_skills.append(skill)
    return required_skills

job_description = "We are looking for a skilled Python developer with experience in AWS, SQL, and JavaScript. Knowledge of HTML, CSS, and Bootstrap is a plus."

required_skills = extract_job_skills(job_description)
print(required_skills)