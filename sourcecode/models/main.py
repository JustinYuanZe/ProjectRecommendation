from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from engine import YZUAdvisorEngine

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
DATA_FILE = os.path.join(project_root, 'data', 'Processed', 'course_data', 'final_mapped_data.json')

advisor = YZUAdvisorEngine(DATA_FILE)
app = FastAPI(title="YZU AI Career Advisor API")

@app.on_event("startup")
def startup_event():
    try:
        advisor.load_resources()
    except Exception as e:
        print(f"Startup error: {e}")

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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)