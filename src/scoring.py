def calculate_score(resume_skills, job_skills):
    matched_skills = set(resume_skills).intersection(set(job_skills))
    matched_count = len(matched_skills)
    required_count = len(job_skills)

    if required_count == 0:
        return 0
    score = (matched_count/required_count)*100
    return score

resume_skills = ["Python","Pandas","SQL"]
job_skills = ["Python","Pandas","SQL","AWS"]

score = calculate_score (resume_skills,job_skills)
print(score)

missing_skills = set(job_skills).difference(set(resume_skills))
print(missing_skills)


