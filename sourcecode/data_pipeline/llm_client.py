import json
import os
import time
from llama_cpp import Llama, LlamaGrammar
import csv
import pandas as pd


MODEL_PATH = "../models/phi-3-mini/phi-3-mini-4k-instruct.Q3_K_M.gguf" 
SKILLS_FILE = "onet_skills.json" 
COURSE_DATA_FILE = "1141學期數位學習課程清單Course List.xlsx - 114-1 Course List.csv"
CACHE_FILE = "processed_features_cache.json"
CHECKPOINT_FREQUENCY = 5 



def load_data():
    try:
       
        df = pd.read_csv(f"../{COURSE_DATA_FILE}") 
        df = df.dropna(subset=['Course Name', 'Description'])
        courses = df.to_dict('records')

        with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
            skills = json.load(f)
            
        return courses, skills
    except FileNotFoundError as e:
        print(f"file: not found: {e}")
        return [], []
    except json.JSONDecodeError:
        print(f"error: File {SKILLS_FILE} is not valid.")
        return [], []

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error, start again")
            return {}
    return {}

def save_cache(cache):
    """Checkpoint"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)
        print(f"\n[CHECKPOINT] saved successfully. Total: {len(cache)}")

# --- HÀM TẠO GBNF GRAMMAR ---

def create_gbnf_grammar(skills):
    """
    GNBF grammar
    """
    skill_rules = [f'"{s}"' for s in skills]
    skill_rules_str = " | ".join(skill_rules)
    
    json_grammar = f"""
    root ::= "{{" ws "reasoning" ws ":" ws string "," ws "skills" ws ":" ws "[" (ws skill_array)? "]" ws "}}"
    skill_array ::= skill (ws "," ws skill)*
    skill ::= {skill_rules_str}
    
    string ::= ["] (
        [^"\\\n] |
        "\\" (["\\/bfnrt] | "u" [0-9a-fA-F]{{4}})
    )* ["]
    
    # Basic definition
    ws ::= [ \\t\\n]*
    """
    return json_grammar


def process_course(llm, grammar, course):
    """
    create prompt
    """
    
    # take skills 
    available_skills = "\n- ".join(json.loads(grammar.options_json)['skill_rules'])
    
    # build System Prompt
    system_prompt = (
        "Bạn là một hệ thống trích xuất đặc trưng (Feature Extractor) chuyên nghiệp. "
        "Nhiệm vụ của bạn là đọc mô tả khóa học và trích xuất các kỹ năng O*NET liên quan. "
        "Bạn PHẢI tuân thủ nghiêm ngặt GBNF Grammar và chỉ trả về các kỹ năng có trong danh sách sau. "
        "Kết quả phải là một đối tượng JSON hoàn chỉnh với hai trường: 'reasoning' (giải thích ngắn gọn) và 'skills' (danh sách các kỹ năng)."
    )
    
    # 
    user_prompt = f"""
    --- KHÓA HỌC ---
    Tên Khóa học: {course.get('Course Name', 'N/A')}
    Mô tả Khóa học: {course.get('Description', 'N/A')}

    --- DANH SÁCH KỸ NĂNG O*NET HỢP LỆ ---
    {available_skills}

    Dựa trên mô tả khóa học, vui lòng trích xuất tối đa 5 kỹ năng O*NET phù hợp nhất.
    """
    
    # Gọi LLM (Sử dụng tham số grammar để buộc định dạng)
    try:
        start_time = time.time()
        
        # LƯU Ý: n_gpu_layers=32 BUỘC MÔ HÌNH CHẠY TRÊN GPU. 
        # Nếu gặp lỗi VRAM, hãy giảm xuống (ví dụ: 25 hoặc 20)
        output = llm.create_completion(
            prompt=user_prompt,
            grammar=grammar,
            max_tokens=2048,
            temperature=0.0, # Nhiệt độ 0.0 để đảm bảo LLM tuân thủ nghiêm ngặt GBNF
            top_p=1.0,
            logprobs=False,
            echo=False,
            stream=False,
            n_gpu_layers=32, 
            system_prompt=system_prompt,
        )
        
        end_time = time.time()
        
        # Trích xuất và phân tích kết quả JSON
        json_output = output['choices'][0]['text']
        data = json.loads(json_output)
        
        print(f" -> OK ({end_time - start_time:.2f}s)")
        return data
        
    except Exception as e:
        print(f" -> LỖI LLM/Parsing: {e}")
        return {"reasoning": "Error during processing", "skills": []}

# --- MAIN EXECUTION ---

def main():
    """Chức năng chính để chạy vòng lặp xử lý."""
    
    print("--- KHỞI ĐỘNG HỆ THỐNG TRÍCH XUẤT ĐẶC TRƯNG LLM ---")
    
    # 1. Tải Dữ liệu
    courses, skills = load_data()
    if not courses or not skills:
        return
    
    # 2. Xây dựng GBNF Grammar và LLM
    gbnf_grammar_str = create_gbnf_grammar(skills)
    grammar = LlamaGrammar.from_string(gbnf_grammar_str)
    
    # Khởi tạo mô hình (Thử thách GPU AMD nằm ở đây)
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096, # Context Window cho Phi-3 Mini
            verbose=False,
        )
        print(f"ĐÃ TẢI MÔ HÌNH: {os.path.basename(MODEL_PATH)} ({len(skills)} kỹ năng O*NET)")
    except Exception as e:
        print(f"\n[LỖI CÀI ĐẶT LLM]: Không thể tải mô hình từ {MODEL_PATH}")
        print(f"Lỗi: {e}")
        print("XIN KIỂM TRA: 1. Đường dẫn file đã đúng chưa. 2. Thư viện llama-cpp-python đã cài đặt đúng (đặc biệt là hỗ trợ AMD GPU/CLBlast).")
        return

    # 3. Tải Checkpoint
    processed_cache = load_cache()
    
    # 4. Bắt đầu Vòng lặp Xử lý
    total_courses = len(courses)
    processed_count = 0
    
    for i, course in enumerate(courses):
        course_id = course.get('Course Name')
        
        if not course_id:
             continue

        # Bỏ qua nếu đã xử lý (Checkpointing)
        if course_id in processed_cache:
            processed_count += 1
            continue

        # Tiến trình
        print(f"\n[{i+1}/{total_courses}] Xử lý: {course_id}")
        
        # Gọi LLM
        result = process_course(llm, grammar, course)
        
        # Lưu kết quả
        processed_cache[course_id] = {
            "name": course_id,
            "description": course.get('Description'),
            "features": result
        }
        processed_count += 1
        
        # 5. Lưu Checkpoint Định kỳ
        if processed_count % CHECKPOINT_FREQUENCY == 0:
            save_cache(processed_cache)

    # Lưu lần cuối
    save_cache(processed_cache)
    print("\n--- HOÀN THÀNH QUÁ TRÌNH TRÍCH XUẤT ĐẶC TRƯNG ---")
    print(f"Tổng số khóa học đã xử lý: {len(processed_cache)}")

if __name__ == "__main__":
    main()