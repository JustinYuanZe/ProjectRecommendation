import pandas as pd
import os
import json
import time
import logging
import sys
from google import genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemma-3-27b-it"
OPTIMAL_RPM = 25
BATCH_SIZE = 10
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('course_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RobustCourseGenerator:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = MODEL_NAME
        self.min_delay = 60.0 / OPTIMAL_RPM
        self.last_request_time = 0

    def enforce_rate_limit(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed + 0.5
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def _get_department_hint(self, department: str, course_code: str) -> str:
        if "Informatics" in department:
            return "Focus on computer science fundamentals, programming, algorithms, and software development."
        
        elif "Computer Science" in department:
            return "Focus on computing theory, software engineering, and practical programming skills."
        
        elif "Information Management" in department:
            return "Focus on business technology, data analytics, and management information systems."
        
        elif "Information Communication" in department:
            return "Focus on multimedia design, digital communication, and human-computer interaction."
        
        elif "Electrical" in department:
            code = str(course_code).upper()
            if any(x in code for x in ['COMM', 'SIGNAL', 'RF']):
                return "Focus on communication systems and signal processing."
            elif any(x in code for x in ['POWER', 'MACHINERY', 'ELECTRONICS']):
                return "Focus on electrical circuits, power systems, and electronics."
            else:
                return "Focus on electrical engineering principles and circuit design."
        
        elif "Management" in department:
            return "Focus on business applications and management principles."
        
        else:
            return "Focus on core concepts and practical applications in the field."

    def validate_response(self, desc: str) -> bool:
        if not desc or len(desc.strip()) < 25:
            return False
        
        invalid_starts = [
            "I'm sorry", "I cannot", "As an AI", 
            "This course", "The course", "In this course",
            "Here is", "Description:"
        ]
        
        if any(desc.startswith(start) for start in invalid_starts):
            return False
        
        if '**' in desc or '#' in desc or '```' in desc:
            return False
        
        return True

    def get_fallback_description(self, course_name: str, department: str) -> str:
        return f"Provides comprehensive coverage of {course_name}, integrating theoretical concepts with practical applications relevant to {department}."

    def generate_course_description(self, course_name: str, course_code: str, 
                                   is_english_taught: bool, department: str) -> str:
        
        dept_hint = self._get_department_hint(department, course_code)
        
        prompt = f"""
        Act as an academic advisor. Write a concise 2-3 sentence course description for:
        
        Course Code: {course_code}
        Course Title: {course_name}
        Department: {department}
        Language: {'English' if is_english_taught else 'Vietnamese'}
        
        Guidelines:
        1. {dept_hint}
        2. Mention 2-3 specific technical concepts or skills.
        3. Use professional academic tone, begin with an action verb.
        4. Keep it practical and career-oriented.
        
        Output ONLY the course description text.
        """
        
        for retry in range(MAX_RETRIES):
            try:
                self.enforce_rate_limit()
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                
                desc = response.text.strip()
                
                if self.validate_response(desc):
                    return desc
                else:
                    logger.warning(f"Invalid response for {course_code}. Retry {retry+1}")
                    
            except Exception as e:
                error_msg = str(e)
                logger.error(f"API error for {course_code}: {error_msg[:100]}")
                
                if "quota" in error_msg.lower() or "429" in error_msg:
                    logger.warning("Quota limit hit. Waiting 70 seconds...")
                    time.sleep(70)
                else:
                    time.sleep(5)
        
        return self.get_fallback_description(course_name, department)

    def process_courses(self, input_file: str, output_file: str):
        if not os.path.exists(input_file):
            logger.error(f"Input file not found at: {input_file}")
            return False
        
        try:
            df = pd.read_csv(input_file)
            
            # Create directory if missing
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            results = []
            progress_file = output_file.replace('.json', '_progress.json')
            
            # Resume Logic
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        progress_data = json.load(f)
                        results = progress_data.get('courses', [])
                        logger.info(f"Resumed {len(results)} previously processed courses")
                except Exception as e:
                    logger.warning(f"Could not load progress: {e}")
            
            processed_codes = {c.get('code') for c in results if c.get('code')}
            total_to_process = len(df)
            
            for idx, row in df.iterrows():
                try:
                    code = str(row['Course_Code']).strip()
                    
                    if code in processed_codes:
                        continue
                    
                    name = str(row['Course_Name']).strip()
                    english = str(row.get('Taught_in_English', 'false')).lower() == 'true'
                    dept = str(row.get('Department', 'General')).strip()
                    
                    logger.info(f"[{idx+1}/{total_to_process}] Processing {code}")
                    
                    desc = self.generate_course_description(name, code, english, dept)
                    
                    course_data = {
                        "id": str(idx + 1),
                        "code": code,
                        "name": name,
                        "description": desc,
                        "taught_in_english": english,
                        "department": dept,
                        "credits": 3,
                        "level": 1,
                        "generated_at": datetime.now().isoformat()
                    }
                    results.append(course_data)
                    
                    if len(results) % BATCH_SIZE == 0:
                        self._save_with_progress(results, output_file, progress_file, idx)
                        logger.info(f"Checkpoint saved: {len(results)} courses")
                        
                except KeyboardInterrupt:
                    logger.warning("Interrupted by user (Ctrl+C). Saving progress...")
                    self._save_with_progress(results, output_file, progress_file, idx)
                    logger.info(f"Progress saved. Processed {len(results)} courses.")
                    sys.exit(0)
                    
                except Exception as e:
                    logger.error(f"Error processing row {idx}: {e}")
                    continue

            # Final Save
            self._save_with_progress(results, output_file, progress_file, len(df)-1, final=True)
            logger.info(f"Completed! Generated {len(results)} course descriptions.")
            return True
            
        except KeyboardInterrupt:
            logger.warning("Interrupted by user (Ctrl+C). Saving progress...")
            if 'results' in locals() and results:
                self._save_with_progress(results, output_file, progress_file, 0)
            sys.exit(0)
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            return False

    def _save_with_progress(self, data, output_file, progress_file, last_index, final=False):
        try:
            if final:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                if os.path.exists(progress_file):
                    os.remove(progress_file)
            else:
                progress_data = {
                    'courses': data,
                    'last_index': last_index,
                    'timestamp': datetime.now().isoformat()
                }
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump(progress_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

def main():
    if not API_KEY or "YOUR_" in API_KEY:
        logger.error("Please set GEMINI_API_KEY in .env file or environment variables")
        return

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    

    project_root = os.path.dirname(os.path.dirname(current_script_dir))

    data_dir = os.path.join(project_root, "data", "Processed", "course_data")
    
    input_file = os.path.join(data_dir, "targeted_data.csv")
    output_file = os.path.join(data_dir, "targeted_courses_final.json")


    print(f"Project Root: {project_root}")
    print(f"Reading from: {input_file}")
    print(f"Writing to:   {output_file}")
    
    generator = RobustCourseGenerator(API_KEY)
    generator.process_courses(input_file, output_file)

if __name__ == "__main__":
    main()