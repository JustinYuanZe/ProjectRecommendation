# ultra_simple_tfidf.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

print(" Loading data...")
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

courses = []
for _, row in courses_df.iterrows():
    program = str(row.get('Program_and_Year', ''))
    title = str(row.get('Course_Title_EN', ''))
    if any(dept in program for dept in target_departments) and title.strip():
        clean_title = title.split('*')[0].strip()
        courses.append(clean_title)

print(f"Courses: {len(courses)}")

# Load 5000 skills
with open("data/Processed/generated_master_skills.txt", 'r', encoding='utf-8') as f:
    skills = [line.strip() for line in f if line.strip()][:5000]

print(f" Skills: {len(skills)}")

print(" Training TF-IDF...")

# Combine all text
all_text = courses + skills

# Create TF-IDF
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
all_vectors = tfidf.fit_transform(all_text).toarray()  

# Split vectors
course_vectors = all_vectors[:len(courses)]
skill_vectors = all_vectors[len(courses):]

print(" Training completed")

print("\n Testing mapping...")

test_courses = [
    "Computer Programming Lab.II",
    "Engineering Drawing", 
    "Materials Science"
]

for course in test_courses:
    # Transform course
    course_vec = tfidf.transform([course]).toarray()
    
    # Calculate similarities
    similarities = cosine_similarity(course_vec, skill_vectors)[0]
    
    # Get top 3
    top_indices = np.argsort(similarities)[-3:][::-1]
    
    print(f"\n {course}:")
    for idx in top_indices:
        if similarities[idx] > 0.1:
            print(f"   - {skills[idx]} ({similarities[idx]:.3f})")

print(f"\nMapping all {len(courses)} courses...")

results = []
for i, course in enumerate(courses):
    if i % 100 == 0:
        print(f"   {i}/{len(courses)}")
    
    course_vec = tfidf.transform([course]).toarray()
    similarities = cosine_similarity(course_vec, skill_vectors)[0]
    top_indices = np.argsort(similarities)[-5:][::-1]
    
    matched_skills = []
    for idx in top_indices:
        if similarities[idx] > 0.1:
            matched_skills.append(skills[idx])
    
    results.append({
        'course': course,
        'skills': ' | '.join(matched_skills[:3])  # Top 3 only
    })

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv('ultra_simple_mappings.csv', index=False, encoding='utf-8')

print(f" Saved {len(results)} mappings to ultra_simple_mappings.csv")
print("DONE!")