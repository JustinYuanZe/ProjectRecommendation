import os
import json
import time
import pandas as pd
from groq import Groq

# --- CONFIGURATION ---
client = Groq() 

INPUT_FILE = "data/Raw/JobsDatasetProcessed.csv"
OUTPUT_FILE = "data/processed/generated_master_skills.txt"

# --- FIX #1: Use the more token-efficient model ---
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
        truncated_description = str(job_description)[:4000] # Use a smaller chunk to save tokens
        print(f"-> Analyzing description for skills...")
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
        return None # Return None on error to signal a retry might be needed

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

    # --- FIX #2: Add Persistence Logic ---
    master_skills_set = set()
    processed_descriptions = set()

    # Load already processed skills if the output file exists
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                master_skills_set.add(line.strip())
        print(f"Loaded {len(master_skills_set)} existing skills from '{OUTPUT_FILE}'. Resuming...")
        # Note: This simple resume doesn't track which descriptions were processed,
        # but it prevents losing the skills already found.

    total_to_process = len(unique_descriptions)
    for i, description in enumerate(unique_descriptions):
        print(f"\nProcessing description {i+1}/{total_to_process}...")
        
        skills = extract_skills_from_description(description)
        
        if skills is None: # API error occurred
            print("!!! API error detected. Stopping script to avoid losing progress.")
            break # Exit the loop safely

        if skills:
            cleaned_skills = {s.strip() for s in skills}
            new_skills_found = len(cleaned_skills - master_skills_set)
            master_skills_set.update(cleaned_skills)
            print(f"   Found {len(cleaned_skills)} skills ({new_skills_found} new).")
        
        # Save progress after every successful API call
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for skill in sorted(list(master_skills_set)):
                f.write(skill + '\n')

        time.sleep(2)

    print(f"\nTotal unique skills generated: {len(master_skills_set)}")
    print(f"✅ --- Finished! Final master skills list is saved at: '{OUTPUT_FILE}' ---")

if __name__ == "__main__":
    main()
