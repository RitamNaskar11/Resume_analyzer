import PyPDF2
import re
def extract_text_from_pdf(pdf_path):
    reader  = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# pdf_path = "data/resume.pdf"


# text = extract_text_from_pdf(pdf_path)
# print(text)

def extract_skills(text):
    section_patterns = r'(?is)(?:skills|technical skills|core skills|technical proficiencies)(.*?)(?=\n\s*(?:experience|education|projects|certifications|achievements|declaration|work experience)\b|$)'

    match = re.search(section_patterns,text)

    if not match:
        return[]
    

    skills_text = match.group(1)

    skills_text = skills_text.replace("\n"," ")
    skills_text = re.sub(r'•', ',', skills_text)
    
    skills_text = re.split(r', |; +',skills_text)



    found_skills = []

            
    return found_skills

# skills = extract_skills(text)
# print(skills)

