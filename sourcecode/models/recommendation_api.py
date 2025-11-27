# recommendation_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommendation_model import CourseRecommender
import uvicorn
import os

app = FastAPI(title="Course Recommendation API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recommendation model
recommender = CourseRecommender()
model_path = "models/recommendation_model.pkl"

if os.path.exists(model_path):
    recommender.load_model('models/recommendation_model')
    print("Recommendation API Ready!")
else:
    print("Model not found. Please train the model first.")
    exit(1)

@app.get("/")
async def root():
    return {
        "message": "Course Recommendation API",
        "status": "active",
        "model_info": {
            "courses": len(recommender.courses),
            "skills": len(recommender.skills)
        }
    }

@app.get("/recommend/course/{course_title}")
async def recommend_by_course(course_title: str, top_k: int = 5):
    """Recommend courses similar to a given course"""
    try:
        recommendations = recommender.recommend_courses(course_title, top_k)
        return {
            "input_course": course_title,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend/skills")
async def recommend_by_skills(skills: list[str], top_k: int = 5):
    """Recommend courses based on skills"""
    try:
        recommendations = recommender.recommend_by_skills(skills, top_k)
        return {
            "input_skills": skills,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses")
async def get_courses(limit: int = 10):
    """Get available courses"""
    return {
        "courses": recommender.courses[:limit],
        "total_courses": len(recommender.courses)
    }

@app.get("/skills")
async def get_skills(limit: int = 10):
    """Get available skills"""
    return {
        "skills": recommender.skills[:limit],
        "total_skills": len(recommender.skills)
    }

if __name__ == "__main__":
    print("Starting Recommendation API...")
    print("Available at: http://localhost:8001")
    print("API Docs at: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)