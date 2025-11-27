# create_training_data.py
import pandas as pd
import json
from simple_tfidf_api import initialize_tfidf, find_skills_for_course

print(" Creating training data for recommendation model...")

initialize_tfidf()
training_data = []

courses_df = pd.read_csv("data/Processed/course_data/cleaned_course_data.csv")
target_departments = [
    "Department of Computer Science and Engineering",
    "International Bachelor Program in Engineering",
    "International Bachelor Program in Electrical and Communication Engineering", 
    "Department of Electrical Engineering",
    "Department of Information Management",
    "Department of Information Communication",
    "International Bachelor Program in Informatics"
]

for _, row in courses_df.iterrows():
    program = str(row.get('Program_and_Year', ''))
    title = str(row.get('Course_Title_EN', ''))
    
    if any(dept in program for dept in target_departments) and title.strip():
        clean_title = title.split('*')[0].strip()
        
        # Map course to skills
        skills = find_skills_for_course(clean_title, top_k=10, min_similarity=0.05)
        
        if skills:
            training_data.append({
                'course_title': clean_title,
                'program': program,
                'matched_skills': [s['skill'] for s in skills],
                'skill_scores': [s['similarity'] for s in skills]
            })

output_path = "data/Processed/training_data.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

print(f" Created training data with {len(training_data)} courses")
print(" Saved to: training_data.json")