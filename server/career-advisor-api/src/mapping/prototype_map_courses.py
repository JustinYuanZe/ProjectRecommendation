import os
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- CONFIGURATION ---
# Paths are relative to the project root (where you run the script)
COURSES_FILE = "data/Processed/course_data/cleaned_course_data.csv"
MASTER_SKILLS_FILE = "data/Processed/generated_master_skills.txt"
OUTPUT_FILE = "data/Processed/prototype_course_skills.jsonl"

# Number of top skills to take from the master list for matching
# We use a smaller set for a prototype to keep it fast
TOP_K_SKILLS = 5000 
# Number of sample courses to process
NUM_SAMPLE_COURSES = 100
# The similarity threshold for a skill to be "matched"
SIMILARITY_THRESHOLD = 0.1 # Lower threshold for TF-IDF

# Filter for relevant departments
RELEVANT_DEPARTMENTS = [
    'Computer Science', 'Information Management', 'Information Communication',
    'Electrical Engineering', 'Informatics'
]

def clean_text(text):
    """A simple function to clean text for TF-IDF."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text) # Remove non-alphanumeric
    text = re.sub(r'\s+', ' ', text) # Condense whitespace
    return text.strip()

def main():
    print("--- Starting Prototype Data Mapping (Local TF-IDF Method) ---")

    # 1. Load Master Skills List
    try:
        with open(MASTER_SKILLS_FILE, 'r', encoding='utf-8') as f:
            master_skills_full = [line.strip() for line in f if line.strip()]
            # We take the top 5000 skills for this prototype to run faster
            master_skills = master_skills_full[:TOP_K_SKILLS]
        print(f"Loaded {len(master_skills)} top skills (out of {len(master_skills_full)} total) for matching.")
    except FileNotFoundError:
        print(f"!!! FATAL ERROR: Master skills file not found at '{MASTER_SKILLS_FILE}'.")
        return

    # 2. Load and Filter Courses
    try:
        df_courses = pd.read_csv(COURSES_FILE)
        pattern = '|'.join(RELEVANT_DEPARTMENTS)
        # Filter for relevant departments and take the first N samples
        df_filtered = df_courses[df_courses['Program_and_Year'].str.contains(pattern, case=False, na=False)].head(NUM_SAMPLE_COURSES)
        
        # Combine English and Chinese titles for more keywords
        df_filtered['course_text'] = df_filtered['Course_Title_EN'].apply(clean_text) + " " + \
                                     df_filtered['Course_Title_CN'].apply(clean_text)
        
        courses_to_process = df_filtered.to_dict('records')
        print(f"Loaded and filtered {len(courses_to_process)} sample courses.")
    except FileNotFoundError:
        print(f"!!! FATAL ERROR: Courses file not found at '{COURSES_FILE}'.")
        return
    except KeyError:
        print("!!! FATAL ERROR: Make sure your CSV has 'Program_and_Year', 'Course_Title_EN', and 'Course_Title_CN' columns.")
        return

    # 3. Setup TF-IDF Vectorizer
    print("Fitting TF-IDF vectorizer...")
    # We fit the vectorizer ONCE on our entire "vocabulary" (all skills + all course text)
    all_text = [clean_text(s) for s in master_skills] + [c['course_text'] for c in courses_to_process]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(all_text)

    # Vectorize the master skills list
    skill_vectors = vectorizer.transform([clean_text(s) for s in master_skills])
    print("Skills list vectorized.")

    # 4. Process Courses and Map Skills
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        for i, course in enumerate(courses_to_process):
            print(f"Processing course {i+1}/{len(courses_to_process)}: {course.get('Course_Title_EN', 'N/A')}...")
            
            if not course['course_text']:
                continue
            
            # Vectorize the single course's text
            course_vector = vectorizer.transform([course['course_text']])
            
            # Calculate cosine similarity between this one course and ALL skills
            similarity_scores = cosine_similarity(course_vector, skill_vectors)[0] # Get the first (and only) row
            
            # Find skills that meet the threshold
            matched_skills = []
            for j, score in enumerate(similarity_scores):
                if score > SIMILARITY_THRESHOLD:
                    matched_skills.append(master_skills[j])
            
            # Save the result
            course_output = course.copy()
            course_output['matched_skills'] = matched_skills
            # Delete the temporary text field
            if 'course_text' in course_output:
                del course_output['course_text']
            
            f_out.write(json.dumps(course_output) + '\n')
            print(f"   -> Found {len(matched_skills)} skills.")

    print(f"\n✅ --- Success! Prototype mapping data saved to '{OUTPUT_FILE}' ---")

if __name__ == "__main__":
    main()