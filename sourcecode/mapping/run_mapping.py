import json
from sentence_transformers import SentenceTransformer, util
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

INPUT_COURSES_FILE = os.path.join(project_root, 'data', 'Processed', 'course_data', 'courses_with_descriptions.json')
SKILLS_FILE = os.path.join(project_root, 'data', 'Processed', 'generated_master_skills.txt')
OUTPUT_FILE = os.path.join(project_root, 'data', 'Processed', 'course_data', 'final_mapped_data.json')

def load_skills_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        skills = [line.strip() for line in f if line.strip()]
    return skills

def main():
    print("Starting course-skill mapping process...")
    
    print("Loading SBERT model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Reading courses file...")
    if not os.path.exists(INPUT_COURSES_FILE):
        print("Error: Courses file not found!")
        return

    with open(INPUT_COURSES_FILE, 'r', encoding='utf-8') as f:
        courses_data = json.load(f)
    
    print(f"Loaded {len(courses_data)} courses.")

    if not os.path.exists(SKILLS_FILE):
        print("Error: Skills file not found!")
        return
    
    skills_list = load_skills_from_txt(SKILLS_FILE)
    print(f"Loaded {len(skills_list)} skills.")

    print("Encoding skills into vectors...")
    skill_embeddings = model.encode(skills_list, convert_to_tensor=True, show_progress_bar=True)

    print("Encoding courses into vectors...")
    course_texts = [f"{c['name']}. {c['description']}" for c in courses_data]
    course_embeddings = model.encode(course_texts, convert_to_tensor=True, show_progress_bar=True)

    print("Mapping courses to skills...")
    hits = util.semantic_search(course_embeddings, skill_embeddings, top_k=10)

    final_output = []
    
    for i, hit in enumerate(hits):
        course = courses_data[i]
        mapped_skills = []
        
        for match in hit:
            score = match['score']
            if score > 0.3:
                skill_name = skills_list[match['corpus_id']]
                mapped_skills.append({
                    "skill": skill_name,
                    "relevance": round(float(score), 4)
                })
        
        mapped_skills.sort(key=lambda x: x['relevance'], reverse=True)
        mapped_skills = mapped_skills[:5]
        
        course['mapped_skills'] = mapped_skills
        final_output.append(course)

    print(f"Saving results to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    total_mappings = sum(len(course['mapped_skills']) for course in final_output)
    avg_mappings = total_mappings / len(final_output)
    
    print("Mapping completed!")
    print(f"Total courses: {len(final_output)}")
    print(f"Total skills: {len(skills_list)}")
    print(f"Average skills per course: {avg_mappings:.2f}")

if __name__ == "__main__":
    main()