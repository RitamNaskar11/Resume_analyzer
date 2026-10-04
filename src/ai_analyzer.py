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
    Analyze this resume against the job description and provide a detailed analysis of the candidate's strengths, weaknesses, and areas for improvement.
    Job Description: {job_description}


Resume: {resume_text}
Missing Skills:{missing_skills}
Matched Skills:{matched_skills}

Give the analysis in the following sections:
1.Strengths
2.Weaknesses
3.Missing Skills:{missing_skills}
- Explain why each missing skill is important for this job.
- If the list is empty, say "No required skills are missing."
4.Suggestions areas for improvement

IMPORTANT:
The Missing Skills section must be based ONLY on the Job Description.
Do NOT use #, *, **, ---, or other Markdown symbols.
Return your analysis in plain text only.


"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", 
        messages=[
            {
            "role": "user", 
            "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
