import re
import json
import pandas as pd

# 1. Load the O*NET text file
df = pd.read_csv('Technology Skills.txt', sep='\t')
df.columns = df.columns.str.strip()

# 2. Extract Commodity Title and Example
df = df[['Commodity Title', 'Example']].dropna()

# List of common generic trailing words to clean up
GENERIC_SUFFIXES = r"\b(software|toolkit|suite|system|systems|tools|tool|program|platform|application|applications|package)\b"

def clean_skill(skill: str) -> str:
    # Convert to lowercase
    s = skill.lower().strip()
    # Remove text inside parentheses (e.g. "(PEET)", "(TSM)")
    s = re.sub(r"\(.*?\)", "", s)
    # Remove generic trailing words
    s = re.sub(GENERIC_SUFFIXES, "", s)
    # Clean whitespace and trailing punctuation
    s = re.sub(r"\s+", " ", s).strip(" .,:;-")
    return s

# Clean skills
df['Clean_Skill'] = df['Example'].apply(clean_skill)

# Drop empty or single-character noise
df = df[df['Clean_Skill'].str.len() > 1]
df = df.drop_duplicates(subset=['Commodity Title', 'Clean_Skill'])

# 3. Group by Commodity Title
domain_dict = {}
for category, group in df.groupby('Commodity Title'):
    skills = group['Clean_Skill'].tolist()
    
    # Expand multi-word items so core technologies are also indexed standalone
    expanded_skills = set()
    for item in skills:
        expanded_skills.add(item)
        # If an item starts with a primary language (e.g., "python ..."), also add the root term
        for root in ["python", "java", "c++", "c#", "r", "sql", "javascript", "html", "css", "react", "tableau"]:
            if re.search(rf"\b{re.escape(root)}\b", item):
                expanded_skills.add(root)

    domain_dict[str(category)] = sorted(expanded_skills)

# 4. Save to domains.json
with open('domains.json', 'w') as f:
    json.dump(domain_dict, f, indent=4)

print("Successfully generated clean domains.json!")