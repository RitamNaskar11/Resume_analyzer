import re

def calculate_score(resume_skills, job_skills):
    matched_skills = []
    missing_skills = []
    for job_skill in job_skills:

        found = False

        for resume_skill in resume_skills:

            pattern = r'(?<!\w)' + re.escape(job_skill) + r'(?!\w)'

            if re.search(pattern, resume_skill, re.IGNORECASE):
                matched_skills.append(job_skill)
                found = True
                break

        if not found:
            missing_skills.append(job_skill)

    required_count = len(job_skills)

    if required_count == 0:
        return 0, [], []

    score = (len(matched_skills) / required_count) * 100

    return score, matched_skills, missing_skills

# score ,  matched_skills, missing_skills = calculate_score (resume_skills,job_skills)
# print(score,missing_skills, matched_skills)








