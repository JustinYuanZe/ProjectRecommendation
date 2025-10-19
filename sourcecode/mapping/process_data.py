import csv
import os

# --- CORRECTED PATHS (relative to project root) ---
RAW_DATA_PATH = "data/Raw/Data regarding occupation and position etc"
OUTPUT_FILE = "data/processed/refined_skills_and_interests.txt"

FILES_TO_PROCESS = {
    "Abilities to Work Activities.txt": "Abilities Element Name",
    "Knowledge.txt": "Element Name",
    "Skills to Work Context.txt": "Skills Element Name",
    "Task Ratings.txt": "Task",
    "Basic Interests to RIASEC.txt": "Basic Interests Element Name",
    "Occupation Data.txt": "Title"
}

def main():
    print("Starting O*NET data refinement process...")
    master_set = set()

    for filename, column_name in FILES_TO_PROCESS.items():
        filepath = os.path.join(RAW_DATA_PATH, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                count = 0
                for row in reader:
                    item = row.get(column_name)
                    if item and item.strip():
                        master_set.add(item.strip())
                        count += 1
                print(f"-> Extracted {count} items from '{filename}'")
        except FileNotFoundError:
            print(f"WARNING: File not found at '{filepath}'. Skipping.")
        except Exception as e:
            print(f"ERROR reading '{filepath}': {e}. Skipping.")

    sorted_master_list = sorted(list(master_set))
    print(f"\nTotal unique items: {len(sorted_master_list)}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for item in sorted_master_list:
            f.write(item + '\n')
    
    print(f"\n✅ Success! Refined list created at: '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()