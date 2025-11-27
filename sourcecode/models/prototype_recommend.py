# simple_model.py
import torch
import torch.nn as nn
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
from scipy import sparse  

class SimpleCourseSkillModel(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=64):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, output_dim)
        )
    
    def forward(self, x):
        return self.network(x)

class SkillPredictor:
    def __init__(self):
        self.vectorizer = None
        self.mlb = None
        self.model = None
        self.skill_list = []
    
    def prepare_data(self, mapped_data):
        """Prepare data from mapped courses"""
        courses = []
        skills = []
        
        for course in mapped_data:
            title = course.get('cleaned_course_title', course.get('Course_Title_EN', ''))
            if title and 'matched_skills' in course and course['matched_skills']:
                courses.append(title)
                skills.append(course['matched_skills'])
        
        return courses, skills
    
    def train(self, mapped_data):
        """Train simple model on mapped data"""
        courses, skills = self.prepare_data(mapped_data)
        
        if len(courses) < 10:
            print(" Not enough data for training")
            return False
        
        # Create TF-IDF features
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        X = self.vectorizer.fit_transform(courses)
        
        # Convert sparse matrix to dense array explicitly
        if sparse.issparse(X):
            X = X.toarray()  
        else:
            X = np.array(X)
        
        # Multi-label binarizer for skills
        self.mlb = MultiLabelBinarizer()
        y = self.mlb.fit_transform(skills)
        self.skill_list = self.mlb.classes_
        
        # Create simple neural network
        self.model = SimpleCourseSkillModel(X.shape[1], y.shape[1])
        
        # Simple training (on CPU)
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)
        
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        self.model.train()
        for epoch in range(100):  # Quick training
            optimizer.zero_grad()
            outputs = self.model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
        
        print(" Model training completed")
        return True
    
    def predict(self, course_title, top_k=5):
        """Predict skills for a course title"""
        if self.vectorizer is None or self.model is None:
            return []
        
        # Extract features
        X = self.vectorizer.transform([course_title])
        
        # Convert sparse matrix to dense array
        if sparse.issparse(X):
            X = X.toarray()  # Và ở đây
        else:
            X = np.array(X)
            
        X_tensor = torch.FloatTensor(X)
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(X_tensor)
            probabilities = torch.sigmoid(outputs).numpy()[0]
        
        # Get top k skills
        top_indices = np.argsort(probabilities)[-top_k:][::-1]
        predicted_skills = []
        
        for idx in top_indices:
            if probabilities[idx] > 0.3:  # Threshold
                predicted_skills.append(self.skill_list[idx])
        
        return predicted_skills
    
    def save_model(self, path="models/simple_model"):
        """Save model and preprocessors"""
        import os
        os.makedirs("models", exist_ok=True)
        
        if self.vectorizer:
            joblib.dump(self.vectorizer, f"{path}_vectorizer.pkl")
        if self.mlb:
            joblib.dump(self.mlb, f"{path}_mlb.pkl")
        if self.model:
            torch.save(self.model.state_dict(), f"{path}_weights.pth")
        
        print(f" Model saved to {path}")
    
    def load_model(self, path="models/simple_model"):
        """Load model and preprocessors"""
        try:
            self.vectorizer = joblib.load(f"{path}_vectorizer.pkl")
            self.mlb = joblib.load(f"{path}_mlb.pkl")
            
            self.model = SimpleCourseSkillModel(
                len(self.vectorizer.get_feature_names_out()),
                len(self.mlb.classes_)
            )
            self.model.load_state_dict(torch.load(f"{path}_weights.pth"))
            self.skill_list = self.mlb.classes_
            
            print(" Model loaded successfully")
            return True
        except Exception as e:
            print(f" Error loading model: {e}")
            return False

# Quick test
if __name__ == "__main__":
    # Load your mapped data
    try:
        with open("data/Processed/enriched_courses_SAMPLE.jsonl", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
    except FileNotFoundError:
        print(" No mapped data found. Please run mapping first.")
        # Create sample data for testing
        data = [
            {
                "cleaned_course_title": "Introduction to Python Programming",
                "matched_skills": ["Python", "Programming", "Algorithms", "Debugging"]
            },
            {
                "cleaned_course_title": "Web Development with JavaScript", 
                "matched_skills": ["JavaScript", "HTML", "CSS", "Web Development"]
            },
            {
                "cleaned_course_title": "Data Analysis with Python",
                "matched_skills": ["Python", "Data Analysis", "Pandas", "Statistics"]
            }
        ]
        print(" Using sample data for testing")
    
    predictor = SkillPredictor()
    if predictor.train(data):
        # Test prediction
        test_courses = [
            "Introduction to Python Programming",
            "Advanced Web Development", 
            "Machine Learning Basics"
        ]
        
        for test_course in test_courses:
            skills = predictor.predict(test_course)
            print(f"Course: {test_course}")
            print(f"Predicted skills: {skills}")
            print("-" * 50)
        
        # Save model
        predictor.save_model()