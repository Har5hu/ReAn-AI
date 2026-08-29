import pandas as pd

# Comprehensive starter dataset across IT, Non-IT, Business, and Soft Skills
skills_data = [
    # --- Soft Skills & Leadership ---
    {"skill_name": "Communication Skills", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Problem Solving", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Teamwork", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Leadership", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Critical Thinking", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Time Management", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Adaptability", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Interpersonal Skills", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Conflict Resolution", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Negotiation", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Active Listening", "category": "Soft Skill", "domain": "General"},
    {"skill_name": "Decision-Making", "category": "Soft Skill", "domain": "General"},

    # --- IT: Data Science & Analytics ---
    {"skill_name": "Python", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "SQL", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Excel", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Tableau", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Power BI", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Pandas", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "NumPy", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Matplotlib", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Scikit-Learn", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Machine Learning", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Data Visualization", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Data Analysis", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Data Cleaning", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Exploratory Data Analysis", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "EDA", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Statistics", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Jupyter Notebook", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "R", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Big Data", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "ETL", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Deep Learning", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "NLP", "category": "Hard Skill", "domain": "IT"},

    # --- IT: Software & Web Development ---
    {"skill_name": "Java", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "JavaScript", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "TypeScript", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "HTML", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "CSS", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "React", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Node.js", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Flask", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Django", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Git", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "GitHub", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "REST API", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "Docker", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "MongoDB", "category": "Hard Skill", "domain": "IT"},
    {"skill_name": "MySQL", "category": "Hard Skill", "domain": "IT"},

    # --- Non-IT: Business, Finance & Accounting ---
    {"skill_name": "Financial Modeling", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Accounting", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Budgeting", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Auditing", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Risk Management", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Project Management", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Market Research", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Financial Reporting", "category": "Hard Skill", "domain": "Non-IT"},

    # --- Non-IT: Marketing, HR & Operations ---
    {"skill_name": "Search Engine Optimization", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "SEO", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Content Marketing", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Social Media Marketing", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Talent Acquisition", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Recruiting", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Supply Chain Management", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "Customer Relationship Management", "category": "Hard Skill", "domain": "Non-IT"},
    {"skill_name": "CRM", "category": "Hard Skill", "domain": "Non-IT"}
]

df = pd.DataFrame(skills_data)
df.to_csv("skills_database.csv", index=False)
print("skills_database.csv created successfully with", len(df), "skills.")