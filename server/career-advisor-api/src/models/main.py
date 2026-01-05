import os
import uvicorn
import sys
import time
import re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AIzaSyAhgxcKQVImAMKA5l7FC3oRuV1CNpF5vQY"

genai.configure(api_key=GEMINI_API_KEY)

project_root = current_dir.parent.parent
DATA_FILE = os.path.join(project_root, "data", "Processed", "course_data", "targeted_courses_final.json")

if not os.path.exists(DATA_FILE):
    print(f"Data file not found: {DATA_FILE}")

try:
    from engine import YZUAdvisorEngine
except ImportError:
    from sourcecode.models.engine import YZUAdvisorEngine

advisor = YZUAdvisorEngine(DATA_FILE)
app = FastAPI(title="YZU Career Advisor API")

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
        print("AI Engine ready")
    except Exception as e:
        print(f"Error loading engine: {e}")

class AnswerItem(BaseModel):
    question: str
    score: int

class AnalysisRequest(BaseModel):
    answers: List[AnswerItem]

def map_score_to_text(score):
    mapping = {
        -2: "Strongly Disagree",
        -1: "Disagree",
        0: "Neutral",
        1: "Agree",
        2: "Strongly Agree"
    }
    return mapping.get(score, "Neutral")

def extract_course_level(course_code):
    match = re.search(r'\d+', str(course_code))
    if match:
        return int(match.group())
    return 9999

def generate_search_query_with_fallback(prompt_text):
    models_to_try = [
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemma-3-27b-it',
        
    ]
    
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(
                prompt_text,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 300,
                }
            )
            
            if response.text:
                clean_text = response.text.strip().replace('"', '').replace("'", "")
                print(f"Success with model: {model_name}")
                return clean_text
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"Model {model_name} failed: {e}")
            time.sleep(1)
            continue
    
    print("All AI models failed. Using fallback query.")
    return "Technology, Computer Science, and Data Analysis algorithms"

@app.post("/api/analyze-career")
async def analyze_career(req: AnalysisRequest):
    if not advisor.is_ready:
        raise HTTPException(status_code=503, detail="Search Engine not loaded")

    user_responses_text = "Student Self-Assessment:\n"
    for item in req.answers:
        text_answer = map_score_to_text(item.score)
        user_responses_text += f"- Question: {item.question}\n  Answer: {text_answer}\n"

    print("Sending data to AI...")
    
    prompt = f"""
    You are an expert Academic Advisor and Curriculum Specialist. Analyze the student's self-assessment responses below to construct a HIGHLY DETAILED and COMPREHENSIVE search query.

    Your goal is to generate a rich text description that will be used for vector similarity search against a university course database.

    GUIDELINES:
    1.  **Filter:** Strictly IGNORE topics marked "Disagree" or "Strongly Disagree". Base the query ONLY on "Agree" and "Strongly Agree".
    2.  **Expand & Elaborate:** Do not just list the interests. You must EXPAND on them using related academic terms.
        * *Example:* If the user likes "coding", do not just write "coding". Instead, write: "software engineering principles, algorithmic problem solving, programming languages, and system architecture."
    3.  **Structure:** Compose a dense, descriptive paragraph (approx. 60-100 words) starting with "I am looking for courses that involve...".
    4.  **Keywords:** Aggressively include specific technical keywords, methodologies, theoretical concepts, and relevant soft skills (e.g., "critical thinking", "project management") implied by the user's answers.
    5.  **Output:** Return ONLY the generated paragraph text. No markdown, no explanations.

    USER RESPONSES:
    {user_responses_text}
    """

    ai_generated_query = generate_search_query_with_fallback(prompt)
    print(f"Generated Query: {ai_generated_query}")

    try:
        recommended_courses = advisor.recommend(ai_generated_query, top_k=6)
        recommended_courses.sort(key=lambda x: extract_course_level(x.get('code', '')))
        
        return {
            "status": "success",
            "ai_summary": ai_generated_query,
            "courses": recommended_courses
        }
    except Exception as e:
        print(f"Search Engine Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "engine_ready": advisor.is_ready}

if __name__ == "__main__":
    print(f"Server running at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)