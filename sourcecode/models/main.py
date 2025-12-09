from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from engine import YZUAdvisorEngine
from fastapi.middleware.cors import CORSMiddleware

DATA_FILE = r"C:\Users\MSI\career-advisor-ai\data\Processed\course_data\targeted_courses_final.json"

if not os.path.exists(DATA_FILE):
    print(f"Error: Data file not found: {DATA_FILE}")

advisor = YZUAdvisorEngine(DATA_FILE)
app = FastAPI(title="YZU AI Career Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Starting server...")
    try:
        advisor.load_resources()
        print("AI Engine ready!")
    except Exception as e:
        print(f"Error loading engine: {e}")

class UserQuery(BaseModel):
    goal: str

@app.post("/recommend")
async def get_recommendation(query: UserQuery):
    if not advisor.is_ready:
        raise HTTPException(status_code=500, detail="AI Engine not ready")
    
    try:
        results = advisor.recommend(query.goal, top_k=30)
        
        return {
            "status": "success",
            "user_goal": query.goal,
            "data": results
        }
    except Exception as e:
        print(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "engine_ready": advisor.is_ready}

if __name__ == "__main__":
    print(f"Server running at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)