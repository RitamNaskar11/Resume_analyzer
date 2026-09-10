from ast import Return
from pydoc import text

from dotenv import load_dotenv
import os
from groq import Groq
from matplotlib import use

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume(resume_text):
    prompt = f"""Analyze this resume and give feedback on the following aspects 
    
    Resume:{resume_text}

    Tell me:

    1. Strengths

    2. Weaknesses

    3.Missing Skills

    4. Suggestions for Improvement
    
    IMPORTANT:
Return the analysis in plain text only.
Do NOT use Markdown.
Do NOT use #, *, **, ---, or any other Markdown symbols.
Use simple numbered headings and bullet points.
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
