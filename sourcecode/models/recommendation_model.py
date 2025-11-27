# recommendation_model.py
import pandas as pd
import numpy as np
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import joblib

class CourseRecommender:
    def __init__(self):
        self.courses = []
        self.skills = []
        self.course_skills_matrix = None
        self.tfidf = None
        self.svd = None
        
    def load_training_data(self, training_file='data/Processed/training_data.json'):
        print("Loading training data...")
        
        with open(training_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        
        self.courses = [item['course_title'] for item in training_data]
        
        # Extract all unique skills
        all_skills = set()
        for item in training_data:
            all_skills.update(item['matched_skills'])
        self.skills = list(all_skills)
        
        print(f"Loaded {len(self.courses)} courses and {len(self.skills)} skills")
        return training_data
    
    def build_course_skills_matrix(self, training_data):
        print("Building course-skills matrix...")
        
        # Create matrix: courses x skills
        self.course_skills_matrix = np.zeros((len(self.courses), len(self.skills)))
        
        skill_to_index = {skill: idx for idx, skill in enumerate(self.skills)}
        
        for i, item in enumerate(training_data):
            for skill in item['matched_skills']:
                if skill in skill_to_index:
                    self.course_skills_matrix[i, skill_to_index[skill]] = 1
        
        print(f"Matrix shape: {self.course_skills_matrix.shape}")
    
    def train(self, training_file='data/Processed/training_data.json'):
        training_data = self.load_training_data(training_file)
        self.build_course_skills_matrix(training_data)
        
        # Use TF-IDF on course titles for content-based features
        self.tfidf = TfidfVectorizer(max_features=500, stop_words='english')
        course_tfidf = self.tfidf.fit_transform(self.courses)
        
        # Combine content-based and collaborative features
        combined_features = np.hstack([course_tfidf.toarray(), self.course_skills_matrix])
        
        # Dimensionality reduction for latent features
        self.svd = TruncatedSVD(n_components=50, random_state=42)
        self.course_embeddings = self.svd.fit_transform(combined_features)
        
        print("Recommendation model trained")
        print(f"Course embeddings: {self.course_embeddings.shape}")
    
    def recommend_courses(self, input_course, top_k=5):
        if self.tfidf is None:
            return []
        
        # Transform input course
        input_tfidf = self.tfidf.transform([input_course])
        
        # Create input features (assuming no known skills for input course)
        input_skills = np.zeros(len(self.skills))
        input_features = np.hstack([input_tfidf.toarray(), input_skills.reshape(1, -1)])
        
        # Transform to latent space
        input_embedding = self.svd.transform(input_features)
        
        # Calculate similarity with all courses
        similarities = cosine_similarity(input_embedding, self.course_embeddings).flatten()
        
        # Get top k courses
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Similarity threshold
                recommendations.append({
                    'course': self.courses[idx],
                    'similarity': float(similarities[idx])
                })
        
        return recommendations
    
    def recommend_by_skills(self, skills_list, top_k=5):
        if self.svd is None:
            return []
        
        # Create skill vector from input
        input_skills = np.zeros(len(self.skills))
        skill_to_index = {skill: idx for idx, skill in enumerate(self.skills)}
        
        for skill in skills_list:
            if skill in skill_to_index:
                input_skills[skill_to_index[skill]] = 1
        
        # Create input features (no course title)
        input_tfidf = np.zeros((1, len(self.tfidf.get_feature_names_out())))
        input_features = np.hstack([input_tfidf, input_skills.reshape(1, -1)])
        
        # Transform to latent space
        input_embedding = self.svd.transform(input_features)
        
        # Calculate similarity
        similarities = cosine_similarity(input_embedding, self.course_embeddings).flatten()
        
        # Get top k courses
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.1:
                recommendations.append({
                    'course': self.courses[idx],
                    'similarity': float(similarities[idx])
                })
        
        return recommendations
    
    def save_model(self, model_path='models/recommendation_model'):
        # Ensure models directory exists
        os.makedirs("models", exist_ok=True)
        
        joblib.dump({
            'tfidf': self.tfidf,
            'svd': self.svd,
            'courses': self.courses,
            'skills': self.skills,
            'embeddings': self.course_embeddings
        }, f'{model_path}.pkl')
        print(f"Model saved to {model_path}.pkl")
    
    def load_model(self, model_path='models/recommendation_model'):
        model_data = joblib.load(f'{model_path}.pkl')
        self.tfidf = model_data['tfidf']
        self.svd = model_data['svd']
        self.courses = model_data['courses']
        self.skills = model_data['skills']
        self.course_embeddings = model_data['embeddings']
        print("Model loaded")

# Train model
if __name__ == "__main__":
    recommender = CourseRecommender()
    recommender.train('data/Processed/training_data.json')
    
    # Test recommendations
    print("Testing recommendations:")
    
    # Test 1: Course-based recommendation
    test_course = "Computer Programming Lab.II"
    recommendations = recommender.recommend_courses(test_course, 3)
    print(f"Courses similar to '{test_course}':")
    for rec in recommendations:
        print(f"  - {rec['course']} ({rec['similarity']:.3f})")
    
    # Test 2: Skill-based recommendation
    test_skills = ["Python", "Programming", "Data Analysis"]
    recommendations = recommender.recommend_by_skills(test_skills, 3)
    print(f"Courses matching skills {test_skills}:")
    for rec in recommendations:
        print(f"  - {rec['course']} ({rec['similarity']:.3f})")
    
    # Save model
    recommender.save_model()