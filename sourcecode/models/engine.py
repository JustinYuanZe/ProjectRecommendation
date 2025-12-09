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
            self.database = json.load(f)

        print(f"Loaded {len(self.database)} courses")
        print(f"Loading AI model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device='cpu')

        print("Creating vector embeddings...")
        search_corpus = []
        
        for course in self.database:
            full_text = f"{course['code']} {course['name']} {course['description']}"
            search_corpus.append(full_text)
        
        self.embeddings = self.model.encode(search_corpus, convert_to_tensor=True)
        self.is_ready = True
        print("Engine ready")

    def recommend(self, user_goal, top_k=30):
        if not self.is_ready:
            raise Exception("Engine not loaded. Call load_resources() first.")

        query_vec = self.model.encode(user_goal, convert_to_tensor=True)
        scores = util.cos_sim(query_vec, self.embeddings)[0]
        
        candidates_k = min(50, len(self.database))
        top_results = torch.topk(scores, k=candidates_k)

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            course = self.database[idx.item()]
            course_code = course.get('code', '')
            
            level = course.get('level', 1)
            match = re.search(r'\d', course_code)
            if match:
                extracted_level = int(match.group())
                if 1 <= extracted_level <= 4:
                    level = extracted_level
            
            response_item = {
                "code": course_code,
                "name": course.get('name', 'Unknown'),
                "description": course.get('description', ''),
                "match_score": round(float(score), 2),
                "level": level,
                "mapped_skills": []
            }
            results.append(response_item)
            
        return results[:top_k]

if __name__ == "__main__":
    TEST_DATA_PATH = r"C:\Users\MSI\career-advisor-ai\data\Processed\course_data\targeted_courses_final.json"
    
    try:
        advisor = YZUAdvisorEngine(TEST_DATA_PATH)
        advisor.load_resources()
        
        print("\n--- TEST 1: Data Scientist ---")
        results = advisor.recommend("I want to analyze big data and use machine learning")
        for c in results[:3]:
            print(f"[{c['match_score']}] {c['code']} - {c['name']}")

        print("\n--- TEST 2: Web Developer ---")
        results = advisor.recommend("I want to build websites and backend api")
        for c in results[:3]:
            print(f"[{c['match_score']}] {c['code']} - {c['name']}")
            
    except Exception as e:
        print(f"Error: {e}")