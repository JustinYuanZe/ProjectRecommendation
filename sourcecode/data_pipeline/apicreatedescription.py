import pandas as pd
import os
import json
import time
from groq import Groq
from typing import List, Dict

class CourseDescriptionGenerator:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)
    
    def generate_course_description(self, course_name: str, course_code: str, is_english_taught: bool) -> str:
        """Generate description for a single course using Groq SDK"""
        
        prompt = f"""
        Create a concise 2-3 sentence course description for a university course.
        
        Course Code: {course_code}
        Course Name: {course_name}
        Taught in English: {'Yes' if is_english_taught else 'No'}
        
        Provide a professional academic description that explains what the course covers and what students will learn.
        Return only the description text.
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            description = completion.choices[0].message.content.strip()
            return description
            
        except Exception as e:
            print(f"❌ Error for {course_code}: {e}")
            # Wait and retry once if it's a rate limit error
            if "rate limit" in str(e).lower():
                print("⏳ Rate limit hit, waiting 30 seconds...")
                time.sleep(30)
                try:
                    completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    description = completion.choices[0].message.content.strip()
                    return description
                except Exception as retry_error:
                    print(f"❌ Retry failed for {course_code}: {retry_error}")
            
            return f"This course covers {course_name}. Students will learn fundamental concepts and practical applications in this field."
    
    def process_all_courses(self, input_file: str, output_file: str):
        """Process ALL courses and generate JSON with descriptions"""
        
        print("📖 Reading course data...")
        df = pd.read_csv(input_file)
        
        courses_to_process = df
        total_courses = len(courses_to_process)
        courses_json = []
        
        print(f"🎯 Generating descriptions for ALL {total_courses} courses...")
        print("⏰ This will take approximately 30-40 minutes due to rate limits...")
        
        for index, row in courses_to_process.iterrows():
            course_code = str(row['Course_Code']).strip()
            course_name = str(row['Course_Name']).strip()
            is_english_taught = bool(row['Taught_in_English'])
            
            print(f"📝 [{index + 1}/{total_courses}] {course_code}: {course_name}")
            
            # Generate description
            description = self.generate_course_description(course_name, course_code, is_english_taught)
            
            # Add to JSON data
            course_data = {
                "code": course_code,
                "name": course_name,
                "description": description,
                "taught_in_english": is_english_taught
            }
            
            courses_json.append(course_data)
            
            # Delay to avoid rate limiting (2 seconds between requests)
            time.sleep(2)
            
            # Progress update and save checkpoint every 10 courses
            if (index + 1) % 10 == 0:
                print(f"✅ Checkpoint: Processed {index + 1}/{total_courses} courses")
                
                # Save partial results as checkpoint
                checkpoint_file = output_file.replace('.json', f'_checkpoint_{index+1}.json')
                with open(checkpoint_file, 'w', encoding='utf-8') as f:
                    json.dump(courses_json, f, indent=2, ensure_ascii=False)
                print(f"💾 Checkpoint saved: {checkpoint_file}")
        
        # Save final JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(courses_json, f, indent=2, ensure_ascii=False)
        
        print(f"🎉 COMPLETED! Processed all {len(courses_json)} courses")
        print(f"💾 Final JSON saved to: {output_file}")
        
        return courses_json

def resume_from_checkpoint():
    """Resume from the last checkpoint"""
    
    API_KEY = "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"
    MODEL = "llama-3.1-8b-instant"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    input_file = os.path.join(project_root, "data", "Processed", "course_data", "course_mapping_summary.csv")
    
    # Find the latest checkpoint
    checkpoint_files = []
    checkpoint_dir = os.path.join(project_root, "data", "Processed", "course_data")
    for file in os.listdir(checkpoint_dir):
        if file.startswith('courses_with_descriptions_checkpoint_') and file.endswith('.json'):
            checkpoint_files.append(file)
    
    if not checkpoint_files:
        print("❌ No checkpoint files found. Starting from beginning.")
        return None
    
    # Get the latest checkpoint
    latest_checkpoint = sorted(checkpoint_files)[-1]
    checkpoint_num = int(latest_checkpoint.split('_')[-1].replace('.json', ''))
    checkpoint_file = os.path.join(checkpoint_dir, latest_checkpoint)
    
    print(f"🔄 Resuming from checkpoint: {checkpoint_file} (course {checkpoint_num})")
    
    # Load checkpoint data
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        courses_json = json.load(f)
    
    # Load remaining courses
    df = pd.read_csv(input_file)
    remaining_courses = df.iloc[checkpoint_num:]
    
    generator = CourseDescriptionGenerator(API_KEY, MODEL)
    
    total_remaining = len(remaining_courses)
    print(f"📊 Remaining courses: {total_remaining}")
    
    for index, row in remaining_courses.iterrows():
        course_code = str(row['Course_Code']).strip()
        course_name = str(row['Course_Name']).strip()
        is_english_taught = bool(row['Taught_in_English'])
        
        current_num = checkpoint_num + (index) + 1
        print(f"📝 [{current_num}/913] {course_code}: {course_name}")
        
        description = generator.generate_course_description(course_name, course_code, is_english_taught)
        
        course_data = {
            "code": course_code,
            "name": course_name,
            "description": description,
            "taught_in_english": is_english_taught
        }
        
        courses_json.append(course_data)
        time.sleep(2)  # Delay between requests
        
        if current_num % 10 == 0:
            print(f"✅ Checkpoint: Processed {current_num}/913 courses")
            
            # Save progress
            output_file = os.path.join(project_root, "data", "Processed", "course_data", "courses_with_descriptions.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(courses_json, f, indent=2, ensure_ascii=False)
            print(f"💾 Progress saved: {output_file}")
    
    # Final save
    output_file = os.path.join(project_root, "data", "Processed", "course_data", "courses_with_descriptions.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(courses_json, f, indent=2, ensure_ascii=False)
    
    print(f"🎉 COMPLETED! Processed all {len(courses_json)} courses")
    return courses_json

def main():
    # Configuration - API KEY được sử dụng trực tiếp trong Groq()
    API_KEY = "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"
    MODEL = "llama-3.1-8b-instant"
    
    # File paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    input_file = os.path.join(project_root, "data", "Processed", "course_data", "course_mapping_summary.csv")
    output_file = os.path.join(project_root, "data", "Processed", "course_data", "courses_with_descriptions.json")
    
    print("🚀 Starting/Restarting Course Description Generation")
    print("=" * 60)
    print(f"API Key: {API_KEY[:20]}...")  # Hiển thị một phần API key để verify
    print(f"Model: {MODEL}")
    print("=" * 60)
    
    # Check if we should resume from checkpoint
    checkpoint_dir = os.path.join(project_root, "data", "Processed", "course_data")
    checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.startswith('courses_with_descriptions_checkpoint_') and f.endswith('.json')]
    
    if checkpoint_files:
        print("🔄 Resuming from checkpoint...")
        courses_json = resume_from_checkpoint()
    else:
        print("🆕 Starting from beginning...")
        generator = CourseDescriptionGenerator(API_KEY, MODEL)
        courses_json = generator.process_all_courses(input_file, output_file)
    
    if courses_json:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! All course descriptions generated!")
        print("=" * 60)
        
        total_courses = len(courses_json)
        english_courses = sum(1 for course in courses_json if course['taught_in_english'])
        
        print(f"📊 Final Statistics:")
        print(f"   Total courses: {total_courses}")
        print(f"   English-taught courses: {english_courses}")
        print(f"   Regular courses: {total_courses - english_courses}")

if __name__ == "__main__":
    main()