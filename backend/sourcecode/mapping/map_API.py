import os
import json
import time
import pandas as pd
from groq import Groq

# --- CONFIGURATION ---

# Input files
COURSES_FILE = "data/Processed/course_data/cleaned_course_data.csv"
MASTER_SKILLS_FILE = "data/Processed/generated_master_skills.txt"

# Output file for this prototype seed data
OUTPUT_FILE = "data/Processed/enriched_courses_SAMPLE.jsonl" 

# Use the fast and efficient model
MODEL_NAME = "llama-3.1-8b-instant" 

# --- PROTOTYPE LIMITS ---
NUM_SAMPLE_COURSES = 10 # We will process 100 courses
TOP_K_SKILLS = 100     # We will only use the top 500 skills from your list

# Filter for relevant departments
RELEVANT_DEPARTMENTS = [
    'Computer Science', 'Information Management', 'Information Communication',
    'Electrical Engineering', 'Informatics'
]

def load_skills():
    """Loads the top K skills from the master list."""
    try:
        with open(MASTER_SKILLS_FILE, 'r', encoding='utf-8') as f:
            all_skills = [line.strip() for line in f if line.strip()]
        # Get the top K skills for our prompt
        prototype_skills = all_skills[:TOP_K_SKILLS]
        print(f"Loaded {len(prototype_skills)} top skills for mapping.")
        return prototype_skills
    except FileNotFoundError:
        print(f"!!! FATAL ERROR: Master skills file not found at '{MASTER_SKILLS_FILE}'.")
        return None

def safe_json_parse(response_str, course_title):
    """Safely parse JSON response with error handling."""
    if not response_str:
        print(f"   -> Warning: Empty response for '{course_title}'")
        return []
    
    try:
        response_data = json.loads(response_str)
        skills = response_data.get("matched_skills", [])
        
        # Validate that skills is a list
        if not isinstance(skills, list):
            print(f"   -> Warning: 'matched_skills' is not a list for '{course_title}'")
            return []
            
        return skills
    except json.JSONDecodeError as e:
        print(f"   -> JSON parsing error for '{course_title}': {e}")
        print(f"   -> Raw response: {response_str}")
        return []

def main():
    print("--- Starting Seed Data Generation (API Method) ---")
    
    master_skills = load_skills()
    if not master_skills:
        return
        
    skills_list_str = ", ".join(master_skills)

    # Define the system prompt, including the small skill list
    system_prompt = f"""
    You are an expert academic advisor. For the given course title, identify the 5 to 7 most relevant skills.
    You MUST choose these skills exclusively from the following master list:

    --- MASTER SKILLS LIST ---
    {skills_list_str}
    --- END OF LIST ---

    Provide the output as a single, clean JSON object with one key "matched_skills".
    Example: {{"matched_skills": ["Skill from list", "Another skill from list"]}}
    """

    try:
        df = pd.read_csv(COURSES_FILE)
        pattern = '|'.join(RELEVANT_DEPARTMENTS)
        df_filtered = df[df['Program_and_Year'].str.contains(pattern, case=False, na=False)].head(NUM_SAMPLE_COURSES)
        print(f"Loaded {len(df_filtered)} sample courses for processing.")
    except Exception as e:
        print(f"!!! FATAL ERROR loading or filtering data: {e}")
        return

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        courses_to_process = df_filtered.to_dict('records')
        
        for i, course_record in enumerate(courses_to_process):
            course_title = course_record.get('Course_Title_EN')
            
            if not isinstance(course_title, str) or not course_title.strip():
                print(f"   -> Skipped record {i+1} (invalid title).")
                continue

            print(f"-> Processing ({i+1}/{len(courses_to_process)}): {course_title}...")
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze this course: '{course_title}'"}
                    ],
                    model=MODEL_NAME,
                    temperature=0.1,
                    response_format={"type": "json_object"},
                )
                
                # Safely extract response content
                response_str = chat_completion.choices[0].message.content
                
                # Safely parse the JSON response
                skills = safe_json_parse(response_str, course_title)
                
                course_record['matched_skills'] = skills
                f_out.write(json.dumps(course_record) + '\n')
                print(f"   -> Success. Found {len(skills)} skills.")

            except Exception as e:
                print(f"!!! ERROR during API call for '{course_title}': {e}")
                # Write the record without skills in case of error
                course_record['matched_skills'] = []
                f_out.write(json.dumps(course_record) + '\n')
            
            time.sleep(2) # Respect API rate limits

    print(f"\n✅ --- Finished! Seed data saved to '{OUTPUT_FILE}' ---")

if __name__ == "__main__":
    main()
