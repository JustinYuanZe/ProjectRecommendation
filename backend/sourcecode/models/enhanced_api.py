# enhanced_api.py
from fastapi import FastAPI
from simple_model import SkillPredictor
import json

app = FastAPI()
predictor = SkillPredictor()

# Load model khi khởi động
@app.on_event("startup")
async def startup_event():
    if not predictor.load_model():
        print(" Could not load model, using rule-based fallback")
        predictor.model = None

@app.post("/predict-skills/")
async def predict_skills(course_title: str):
    """Predict skills using DL model with fallback"""
    if predictor.model is not None:
        # Use DL model
        skills = predictor.predict(course_title)
        method = "dl_model"
    else:
        # Fallback to rule-based
        from prototype_api import simple_skill_mapper
        result = simple_skill_mapper(course_title)
        skills = result['matched_skills']
        method = "rule_based"
    
    return {
        "course_title": course_title,
        "predicted_skills": skills,
        "method_used": method
    }