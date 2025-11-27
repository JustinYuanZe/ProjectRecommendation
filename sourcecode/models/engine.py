# engine.py
import json
import os
import torch
import re
from sentence_transformers import SentenceTransformer, util

class YZUAdvisorEngine:
    def __init__(self, data_path, model_name='all-MiniLM-L6-v2'):
        self.data_path = data_path
        self.model_name = model_name
        self.database = []
        self.model = None
        self.embeddings = None
        self.is_ready = False

    def load_resources(self):
        print(f"Loading data from: {self.data_path}")
        
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        with open(self.data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        cleaned_data = []
        for course in raw_data:
            seen_skills = set()
            unique_mapped_skills = []
            for skill_data in course.get('mapped_skills', []):
                skill_lower = skill_data['skill'].lower()
                if skill_lower not in seen_skills:
                    seen_skills.add(skill_lower)
                    unique_mapped_skills.append(skill_data)
            course['mapped_skills'] = unique_mapped_skills
            cleaned_data.append(course)
        
        self.database = cleaned_data
        print(f"Loaded {len(self.database)} courses")

        print(f"Loading AI model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device='cpu')

        print("Creating vector embeddings...")
        search_corpus = []
        for course in self.database:
            skills_str = " ".join([s['skill'] for s in course.get('mapped_skills', [])])
            full_text = f"{course['name']} {course['name']} {course['name']}. {course['description']} {skills_str}"
            search_corpus.append(full_text)
        
        self.embeddings = self.model.encode(search_corpus, convert_to_tensor=True)
        self.is_ready = True
        print("Engine ready")

    def recommend(self, user_goal, top_k=30):
        if not self.is_ready:
            raise Exception("Engine not loaded. Call load_resources() first.")

        query_vec = self.model.encode(user_goal, convert_to_tensor=True)
        scores = util.cos_sim(query_vec, self.embeddings)[0]
        
        # Get top 50 candidates first
        candidates_k = 50
        top_results = torch.topk(scores, k=candidates_k)

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            course = self.database[idx.item()]
            course_code = course.get('code', '')
            
            # Extract course level from course code
            level = 99
            match = re.search(r'\d', course_code)
            if match:
                level = int(match.group())
            
            response_item = {
                "code": course_code,
                "name": course.get('name', 'Unknown'),
                "description": course.get('description', ''),
                "mapped_skills": course.get('mapped_skills', []),
                "match_score": round(float(score), 2),
                "level": level
            }
            results.append(response_item)
            
        return results[:top_k]

if __name__ == "__main__":
    TEST_DATA_PATH = r"c:\Users\MSI\career-advisor-ai\data\Processed\course_data\final_mapped_data.json"
    
    try:
        advisor = YZUAdvisorEngine(TEST_DATA_PATH)
        advisor.load_resources()
        
        print("\n--- TEST ---")
        query = "I want to learn Artificial Intelligence"
        results = advisor.recommend(query)
        
        for course in results:
            print(f"[{course['match_score']}] | {course['code']:<10} | {course['name']}")
            
    except Exception as e:
        print(f"Error: {e}")