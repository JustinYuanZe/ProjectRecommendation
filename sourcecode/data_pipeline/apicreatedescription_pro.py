import pandas as pd
import os
import json
import time
import google.generativeai as genai

API_KEY = "AIzaSyCMBTsFKOOlc1VLh4yZhfEu6aZufRuqTf0"
MODEL_NAME = "gemma-3-27b-it"

class CourseDescriptionGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(MODEL_NAME)
    
    def generate_course_description(self, course_name: str, course_code: str, is_english_taught: bool) -> str:
        dept_hint = ""
        code_prefix = str(course_code)[:2].upper()
        
        if code_prefix in ['CS', 'IN', 'IM', 'CI', 'EG', 'EN']:
            dept_hint = "Focus on software engineering, algorithms, coding practices."
        elif code_prefix in ['EE', 'DE', 'ME']:
            dept_hint = "Focus on hardware, circuits, signals, and engineering principles."
        else:
            dept_hint = "Focus on academic and practical applications."

        prompt = f"""
        Write a 2-3 sentence description for:
        Course: {course_code} - {course_name}
        Taught in English: {'Yes' if is_english_taught else 'No'}
        
        Requirements:
        1. {dept_hint}
        2. Include 3 technical keywords.
        3. Professional tone. Start with a verb.
        Output ONLY the text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" not in str(e) and "quota" not in str(e).lower():
                print(f"API Error ({course_code}): {e}")
            
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit! Waiting 30 seconds...")
                time.sleep(30)
                try:
                    return self.model.generate_content(prompt).text.strip()
                except:
                    pass
            
            return f"Advanced study of {course_name}, providing essential skills for future careers."

    def process_all_courses(self, input_file: str, output_file: str, test_mode: bool = False):
        print(f"Reading input file: {input_file}")
        try:
            df = pd.read_csv(input_file)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []

        courses_json = []
        start_index = 0

        if os.path.exists(output_file) and not test_mode:
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list) and len(existing_data) > 0:
                        courses_json = existing_data
                        start_index = len(courses_json)
                        print(f"Found existing file with {start_index} courses.")
                        print(f"Resuming from ID {start_index + 1}...")
            except Exception as e:
                print(f"Error reading existing file, starting fresh. Error: {e}")

        if start_index > 0:
            df_remaining = df.iloc[start_index:]
        else:
            df_remaining = df

        if test_mode:
            print("TEST MODE: Processing first 3 courses")
            df_remaining = df_remaining.head(3)

        total_courses = len(df)
        
        for index, row in df_remaining.iterrows():
            code = str(row['Course_Code']).strip()
            name = str(row['Course_Name']).strip()
            english = str(row['Taught_in_English']).lower() == 'true'
            
            print(f"Processing [{index + 1}/{total_courses}]: {code} - {name}")
            
            desc = self.generate_course_description(name, code, english)
            
            if "Advanced study of" in desc:
                print("   Fallback description")
            else:
                print(f"   OK: {desc[:50]}...")

            new_course = {
                "id": str(index + 1),
                "code": code,
                "name": name,
                "description": desc,
                "taught_in_english": english,
                "credits": 3,
                "level": 1
            }
            
            courses_json.append(new_course)
            time.sleep(2)
            
            if (index + 1) % 5 == 0:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(courses_json, f, indent=2, ensure_ascii=False)
                print(f"   Saved checkpoint ({len(courses_json)} courses)")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(courses_json, f, indent=2, ensure_ascii=False)
        
        print(f"\nCOMPLETED! Total {len(courses_json)} courses. File: {output_file}")

def main():
    input_file = r"C:\Users\MSI\career-advisor-ai\data\Processed\course_data\targeted_data.csv"
    output_file = r"C:\Users\MSI\career-advisor-ai\data\Processed\course_data\targeted_courses_final.json"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    if "YOUR_GEMINI_API_KEY_HERE" in API_KEY:
        print("Error: Please enter your Gemini API Key")
        return

    gen = CourseDescriptionGenerator(API_KEY)
    gen.process_all_courses(input_file, output_file, test_mode=False)

if __name__ == "__main__":
    main()