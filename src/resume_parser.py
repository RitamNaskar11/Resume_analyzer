import PyPDF2
import re
def extract_text_from_pdf(pdf_path):
    reader  = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

pdf_path = "data/resume.pdf"


text = extract_text_from_pdf(pdf_path)
print(text)

def extract_skills(text):
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

    found_skills = []
    for skill in skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

skills = extract_skills(text)
print(skills)

