import fitz  # PyMuPDF for PDF text extraction
import re
from datetime import datetime

# 🔹 Predefined Skills
predefined_skills = set([
    "problem solving", "critical thinking", "business analysis", "data analysis",
    "decision making", "strategic thinking", "business strategy", "market research",
    "competitive analysis", "risk management", "presentation skills", "client management",
    "project management", "benchmarking", "gap analysis", "leadership", "communication",
    "public speaking", "negotiation", "persuasion", "team collaboration",
    "financial modeling", "data visualization", "statistics", "quantitative analysis",
    "qualitative analysis", "microsoft excel", "sql", "power bi", "tableau",
    "python", "sap", "erp systems", "cloud computing", "powerpoint",
    "microsoft project", "jira", "asana", "trello", "crm systems", "scrum",
    "lean six sigma", "change management", "agile methodology", "digital transformation",
    "supply chain management", "customer experience strategy", "brand positioning",
    "pricing strategy", "mergers and acquisitions", "corporate restructuring",
    "emotional intelligence", "adaptability", "time management", "persuasion skills",
    "networking", "contract negotiation", "compliance management", "due diligence",
    "marketing automation", "customer journey mapping", "blockchain", "iot",
    "artificial intelligence", "machine learning", "sustainability consulting"
])

# 🔹 Consulting Firms
consulting_firms = [
    "Boston Consulting Group", "McKinsey & Company", "Bain & Company", "Kearney",
    "Accenture", "Deloitte", "KPMG", "PwC", "TSMG", "OliverWyman", "Alvarez & Marsal",
    "Strategy&", "Roland Berger", "Capgemini E.L.I.T.E", "Parthenon Group",
    "Arthur D. Little", "Frost & Sullivan", "ZS Associates", "IBM"
]

# 🔹 Extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF
    text = " ".join(page.get_text("text") for page in doc)  # Extract text from all pages
    return text.strip()

# 🔹 Preprocess text (removes special characters, converts to lowercase)
def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    return text.lower()  # Convert to lowercase

# 🔹 Extract Name (Assumption: Name appears at the top)
def extract_name(resume_text):
    lines = resume_text.split("\n")[:5]  # Look at the first 5 lines
    for line in lines:
        words = line.strip().split()
        if len(words) >= 2 and words[0][0].isupper() and words[1][0].isupper():
            return line.strip()
    return "Not Found"

# 🔹 Extract Email using Regex
def extract_email(resume_text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, resume_text)
    return match.group(0) if match else "Not Found"

# 🔹 Find Matching Skills
def find_matching_skills(resume_text):
    resume_text = preprocess_text(resume_text)  # Preprocess resume text
    words_in_resume = set(resume_text.split())  # Convert text to a set of words

    matched_skills = {skill for skill in predefined_skills if skill in words_in_resume}
    
    return list(matched_skills)

# 🔹 Extract Companies
def extract_companies(resume_text):
    found_companies = [company for company in consulting_firms if company.lower() in resume_text.lower()]
    return found_companies

import re
from datetime import datetime

def parse_date(date_str):
    """
    Parses date strings like "JUNE 2016", "06/2016", "Jun 2016", or "2 0 1 3 — J U N E 2 0 1 6".
    """
    # Normalize the date string by removing extra spaces
    date_str = re.sub(r"\s+", " ", date_str).strip().lower()

    # Fix split-year issue: Convert "2 0 1 3" -> "2013"
    date_str = re.sub(r"(\d)\s+(\d)\s+(\d)\s+(\d)", r"\1\2\3\4", date_str)

    # Handling different formats: "June 2016", "JUN 2016", "06/2016"
    patterns = [
        (r"([a-zA-Z]+)\s+(\d{4})", "%B %Y"),  # Full month name (e.g., "June 2016")
        (r"([a-zA-Z]{3})\s+(\d{4})", "%b %Y"),  # Abbreviated month (e.g., "Jun 2016")
        (r"(\d{1,2})/(\d{4})", "%m/%Y"),  # Numeric format (e.g., "06/2016")
        (r"(\d{4})", "%Y")
    ]

    for pattern, date_format in patterns:
        match = re.match(pattern, date_str)
        if match:
            try:
                return datetime.strptime(" ".join(match.groups()), date_format)
            except ValueError:
                continue  # Skip invalid formats

    return None  # Return None if parsing fails

# 🔹 Detect and remove the Education section
def remove_education_section(resume_text):
    education_keywords = ["education", "bachelor", "master", "degree", "institute", 
                          "university", "college", "phd", "mba", "b.tech", "m.tech"]
    
    lines = resume_text.split("\n")
    filtered_lines = []
    ignore = False
    
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            ignore = True  # Start ignoring text from "Education" section
        elif ignore and line.strip() == "":  # Stop ignoring when a blank line is found (assuming new section starts)
            ignore = False
        elif not ignore:
            filtered_lines.append(line)
    
    return "\n".join(filtered_lines)

def extract_work_experience(resume_text):
    today = datetime.today()

    # Remove education section to avoid parsing education dates
    filtered_text = remove_education_section(resume_text)
    
    # Regex pattern to find date ranges (Including "2 0 1 3 — J U N E 2 0 1 6")
    experience_pattern = re.compile(
        r"(\b[a-zA-Z]{3,9}\s+\d{4}|\d{1,2}/\d{4}|\d\s+\d\s+\d\s+\d)\s*[-—]\s*(\b[a-zA-Z]{3,9}\s+\d{4}|\d{1,2}/\d{4}|current)", 
        re.IGNORECASE
    )

    total_experience_months = 0

    matches = experience_pattern.findall(filtered_text)
    for start_str, end_str in matches:
        start_date = parse_date(start_str)
        end_date = today if re.search(r"current", end_str, re.IGNORECASE) else parse_date(end_str)

        if start_date and end_date:
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            total_experience_months += max(0, months)  # Prevent negative values

    # Convert total months to years only
    years = total_experience_months // 12

    return f"{years} years" if years > 0 else "Unable to determine"



# 🔹 Main function to process the resume PDF
def process_resume(pdf_path):
    resume_text = extract_text_from_pdf(pdf_path)  # Extract text from PDF
    name = extract_name(resume_text)  # Extract Name
    email = extract_email(resume_text)  # Extract Email
    matched_skills = find_matching_skills(resume_text)  # Find Skills
    found_companies = extract_companies(resume_text)  # Find Companies
    consulting_experience = extract_work_experience(resume_text)
    
    return {
        "Name": name,
        "Email": email,
        "Skills": matched_skills,
        "Companies": found_companies,
        "Consulting Experience": consulting_experience
    }

# 🔹 Run the script with a sample resume
pdf_path = r"C:\Users\MANAS SINGH\OneDrive\Desktop\ResumeParser\Shah_Faisal_Mohammed_Training Leader 3.pdf"  # Replace with actual file path
resume_data = process_resume(pdf_path)

# 🔹 Print Extracted Information
print("Extracted Information:")
print(resume_data)
