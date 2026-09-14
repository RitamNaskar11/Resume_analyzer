from ast import Return
from pydoc import text

from dotenv import load_dotenv
import os
from groq import Groq
from matplotlib import use

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume(resume_text, job_description, matched_skills, missing_skills):
    prompt = f"""
    Analyze this resume against the given job description.
    
    Resume:{resume_text}
    Job Descrption:{job_description}
    Matched Skills:{matched_skills}
    Missing Skills:{missing_skills}

    Compare the resume with the job description carefully.

Tell me:

1. Strengths
- Explain what is strong in the resume and relevant to the job.

2. Weaknesses
- Explain weaknesses or gaps in the resume specifically for this job.

3. Missing Skills
- The program has already identified these missing skills:{missing_skills}
- Analyze ONLY these missing skills.

- Explain why each missing skill is important for this job.

- Do not add any other skills.

- If the list is empty, say "No required skills are missing." 

- List ONLY the skills or requirements mentioned in the Job Description , that are missing from the Resume.

- Do NOT suggest additional skills that are not required by the Job Description.

- If all required skills are present in the Resume, write:"No required skills are missing."

4. Suggestions for Improvement
- Give suggestions specifically for improving the resume for this job.

IMPORTANT:
The Missing Skills section must be based ONLY on the Job Description.
Do not add general or unrelated skills.
Return the analysis in plain text only.
Do NOT use Markdown.
Do NOT use #, *, **, ---, or other Markdown symbols.

"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
