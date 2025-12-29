import os
import json
import time
import pandas as pd
from groq import Groq

# --- CONFIGURATION ---
client = Groq() 

# Corrected paths based on your file structure
INPUT_FILE = "data/Raw/JobsDatasetProcessed.csv"
OUTPUT_FILE = "data/processed/generated_master_skills.txt"
PROGRESS_FILE = "data/processed/progress_tracker.txt" 

# Using the efficient model to avoid daily limits
MODEL_NAME = "llama-3.1-8b-instant"

IT_CS_KEYWORDS = [
    'Computer', 'Software', 'Data', 'Network', 'Developer', 'Programmer', 
    'Information', 'Web', 'Database', 'Cybersecurity', 'Systems', 'Architect',
    'IT', 'Integration', 'Technologist', 'Engineer'
]

def extract_skills_from_description(job_description):
    """Sends a job description to the Groq API and extracts skills."""
    system_prompt = """
    You are an expert technical recruiter. Analyze the job description and extract the top 7-10 most important, marketable skills.
    Include technical skills, soft skills, and specific tools/software.
    Provide the output as a single, clean JSON object with one key: "skills", an array of strings.
    Example: {"skills": ["Java", "Spring Boot", "Agile Methodologies", "Problem Solving", "Docker"]}
    """
    
    
    try:
        truncated_description = str(job_description)[:4000] 
        # print(f"-> Analyzing description for skills...") # Commented out for a cleaner log
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Job Description: {truncated_description}"}
            ],
            model=MODEL_NAME, temperature=0.1, response_format={"type": "json_object"},
        )
        response_str = chat_completion.choices[0].message.content
        if response_str:
            return json.loads(response_str).get("skills", [])
        return []
    except Exception as e:
        print(f"!!! ERROR during API call: {e}")
        return None

def main():
    print("--- Starting Stage 1: Generating master skills list... ---")

    try:
        df = pd.read_csv(INPUT_FILE)
        df.columns = df.columns.str.strip()
        pattern = '|'.join(IT_CS_KEYWORDS)
        df_filtered = df[df['Job Title'].str.contains(pattern, case=False, na=False)]
        unique_descriptions = df_filtered['Description'].dropna().unique()
        print(f"Filtered down to {len(unique_descriptions)} unique IT/CS job descriptions.")
    except Exception as e:
        print(f"!!! FATAL ERROR loading or filtering data: {e}")
        return

    master_skills_set = set()
    start_index = 0

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            master_skills_set.update(line.strip() for line in f)
        print(f"Loaded {len(master_skills_set)} existing skills from '{OUTPUT_FILE}'.")

    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            try:
                start_index = int(f.read().strip())
                print(f"Resuming from record number {start_index + 1}...")
            except (ValueError, IndexError):
                start_index = 0

    total_to_process = len(unique_descriptions)
    
    for i in range(start_index, total_to_process):
        description = unique_descriptions[i]
        print(f"\nProcessing description {i + 1}/{total_to_process}...")
        
        skills = extract_skills_from_description(description)
        
        if skills is None:
            print("!!! API error detected. Stopping script to save progress.")
            break 

        if skills:
            cleaned_skills = {s.strip() for s in skills}
            new_skills_found = len(cleaned_skills - master_skills_set)
            master_skills_set.update(cleaned_skills)
            print(f"   Found {len(cleaned_skills)} skills ({new_skills_found} new).")
        
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f_progress:
            f_progress.write(str(i + 1))
            
        time.sleep(2)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for skill in sorted(list(master_skills_set)):
            f.write(skill + '\n')
    
    print(f"\nTotal unique skills generated: {len(master_skills_set)}")
    print(f"✅ --- Finished or paused! Progress saved. Final list is at: '{OUTPUT_FILE}' ---")

if __name__ == "__main__":
    main()
