# simple_tfidf_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uvicorn

app = FastAPI(title="Course Skills API", version="1.0")

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for TF-IDF data
courses = []
skills = []
tfidf = None
course_vectors = None
skill_vectors = None

def initialize_tfidf():
    global courses, skills, tfidf, course_vectors, skill_vectors
    
    print("Initializing TF-IDF model...")
    
    # Load courses
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

    print(f"Loaded {len(courses)} courses")

    # Load skills
    with open("data/Processed/generated_master_skills.txt", 'r', encoding='utf-8') as f:
        skills = [line.strip() for line in f if line.strip()][:5000]

    print(f"Loaded {len(skills)} skills")

    # Train TF-IDF
    all_text = courses + skills
    tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
    all_vectors = tfidf.fit_transform(all_text).toarray()
    
    course_vectors = all_vectors[:len(courses)]
    skill_vectors = all_vectors[len(courses):]
    
    print("TF-IDF model ready!")

def find_skills_for_course(course_title, top_k=5, min_similarity=0.1):
    if tfidf is None:
        return []
    
    # Transform course to TF-IDF
    course_vec = tfidf.transform([course_title]).toarray()
    
    # Calculate similarities
    similarities = cosine_similarity(course_vec, skill_vectors)[0]
    
    # Get top matches
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        if similarities[idx] > min_similarity:
            results.append({
                'skill': skills[idx],
                'similarity': float(similarities[idx])
            })
    
    return results

# Initialize when starting
initialize_tfidf()

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Course Skills Mapping API",
        "status": "active",
        "data_stats": {
            "courses": len(courses),
            "skills": len(skills)
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": tfidf is not None}

@app.get("/map/{course_title}")
async def map_course(course_title: str, top_k: int = 5, min_similarity: float = 0.1):
    try:
        skills = find_skills_for_course(course_title, top_k, min_similarity)
        
        return {
            "course_title": course_title,
            "matched_skills": skills,
            "total_matches": len(skills),
            "parameters": {
                "top_k": top_k,
                "min_similarity": min_similarity
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/courses")
async def get_courses(limit: int = 10, search: str = None):
    course_list = courses[:limit]
    
    if search:
        course_list = [c for c in courses if search.lower() in c.lower()][:limit]
    
    return {
        "total_courses": len(courses),
        "courses": course_list
    }

@app.get("/skills")
async def get_skills(limit: int = 10):
    return {
        "total_skills": len(skills),
        "skills": skills[:limit]
    }

@app.post("/map-batch")
async def map_batch(course_titles: list[str], top_k: int = 5, min_similarity: float = 0.1):
    results = []
    for title in course_titles:
        skills = find_skills_for_course(title, top_k, min_similarity)
        results.append({
            "course_title": title,
            "matched_skills": skills
        })
    
    return {
        "total_courses": len(results),
        "results": results
    }

if __name__ == "__main__":
    print("Starting Course Skills API...")
    print("Available at: http://localhost:8000")
    print("API Docs at: http://localhost:8000/docs")
    
    uvicorn.run("simple_tfidf_api:app", host="0.0.0.0", port=8000, reload=True)