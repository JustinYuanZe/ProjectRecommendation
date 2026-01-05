import pandas as pd
import re
import os

# --- Setup File Paths ---
# Assuming the script runs from a folder like 'data_pipeline' 
# and the CSV is in '../data/Processed/course_data'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_CSV_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'Processed', 'course_data')

input_file = os.path.join(PROCESSED_CSV_DIR, 'all_course_listings.csv')
output_file = os.path.join(PROCESSED_CSV_DIR, 'cleaned_course_data.csv')

def clean_data(input_filepath, output_filepath):
    """
    Loads the raw course data, cleans noisy rows, removes empty columns, 
    and splits complex features into clean, separate columns.
    """
    print(f"--- Starting Data Cleaning Process ---")
    print(f"Loading raw data from: {input_filepath}")
    
    try:
        # Load the raw CSV. Since the original HTML tables had inconsistent 
        # headers, we use the raw column numbers for initial cleanup.
        df = pd.read_csv(input_filepath, header=None, encoding='utf-8', low_memory=False)
        
        # 1. Map important columns based on their known index positions in the raw file
        # This mapping is essential because pd.read_html often assigns generic column names (0, 1, 2...)
        df.rename(columns={
            0: 'Original_Index',
            1: 'Course_Code_and_Section',
            2: 'Program_and_Year_Raw',
            3: 'Course_Title_Raw',
            4: 'Course_Type',
            5: 'Schedule_and_Credits_Raw',
            6: 'Instructor_Raw',
            # We also identify the metadata columns added by the previous script
            df.shape[1] - 3: 'Semester',
            df.shape[1] - 2: 'Department_ID_Name',
            df.shape[1] - 1: 'File_Source_ID' 
        }, inplace=True)
        
        print(f"Total rows before cleaning: {len(df)}")

        # 2. Filter out noisy rows containing "Selection message"
        initial_clean_len = len(df)
        df = df[~df['Course_Code_and_Section'].astype(str).str.contains('Selection message', na=False)]
        
        removed_rows = initial_clean_len - len(df)
        print(f"Removed {removed_rows} noisy 'Selection message' rows.")

        # 3. Remove columns that are almost entirely empty (NaN)
        # We keep a column only if at least 5% of its data is NOT NaN
        threshold = len(df) * 0.05 
        df.dropna(axis=1, thresh=threshold, inplace=True)
        
        print(f"Dropped empty columns. Dataset width reduced.")

        # --- Feature Decomposition (Splitting Complex Data) ---

        # 4. Split 'Course_Code_and_Section' (e.g., 'EL314 A')
        df[['Course_Code', 'Section']] = df['Course_Code_and_Section'].astype(str).str.split(' ', n=1, expand=True)
        df.drop('Course_Code_and_Section', axis=1, inplace=True)

        # 5. Split Instructor Names (Chinese and English)
        def extract_instructor_names(raw_name):
            if pd.isna(raw_name):
                return None, None
            
            raw_name = str(raw_name).strip()
            
            # Extract Chinese Name (often before the parenthesis)
            match_cn = re.match(r"(.+?)\s*\(", raw_name)
            chinese_name = match_cn.group(1).strip() if match_cn else raw_name.replace('()', '').strip()
            
            # Extract English Name (the content inside the parenthesis)
            match_en = re.search(r"\((.+?)\)", raw_name)
            english_name = match_en.group(1).strip() if match_en else None
            
            return chinese_name, english_name

        df[['Instructor_CN', 'Instructor_EN']] = df['Instructor_Raw'].apply(
            lambda x: pd.Series(extract_instructor_names(x))
        )
        df.drop('Instructor_Raw', axis=1, inplace=True)
        
        # 6. Split Course Titles (Chinese and English)
        # Assumes format: Chinese Title (Syllabus) English Title
        df[['Course_Title_CN', 'Course_Title_EN']] = df['Course_Title_Raw'].astype(str).str.split('\(Syllabus\)', n=1, expand=True)
        
        # Clean up the English title string
        df['Course_Title_EN'] = df['Course_Title_EN'].str.replace(')', '').str.replace('(', '').str.strip()
        df['Course_Title_CN'] = df['Course_Title_CN'].str.strip()
        df.drop('Course_Title_Raw', axis=1, inplace=True)
        
        # 7. Final Clean-up for other metadata columns
        df['Program_and_Year'] = df['Program_and_Year_Raw'].astype(str).str.replace('\"', '').str.strip()
        df.drop('Program_and_Year_Raw', axis=1, inplace=True)

        # Ensure we don't include rows where primary data (Code or Title) is still missing
        df.dropna(subset=['Course_Code', 'Course_Title_CN'], inplace=True)
        
        # 8. Define and reorder the final columns for a logical, clean dataset
        final_columns = [
            'Semester', 
            'Department_ID_Name', # Contains the department code and name info from filename
            'Program_and_Year', # Contains the department name and year/level from the table content
            'Course_Code', 
            'Section', 
            'Course_Title_CN', 
            'Course_Title_EN', 
            'Course_Type', 
            'Instructor_CN', 
            'Instructor_EN', 
            'Schedule_and_Credits_Raw', # This still needs advanced parsing, keeping it raw for now
        ]
        
        # Filter columns to ensure only existing ones are included after dropping NaNs
        final_columns = [col for col in final_columns if col in df.columns]

        df_cleaned = df[final_columns].copy()
        
        print(f"Total structured rows saved: {len(df_cleaned)}")

        # 9. Save the cleaned dataset
        df_cleaned.to_csv(output_filepath, index=False, encoding='utf-8')
        print(f"\nSUCCESS. Cleaned data saved to: {output_filepath}")

    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_filepath}. Ensure 'all_course_listings.csv' exists.")
    except Exception as e:
        print(f"GENERAL ERROR during data cleaning: {e}")
        
if __name__ == "__main__":
    # Ensure the directory exists before attempting to save the file
    if not os.path.exists(PROCESSED_CSV_DIR):
        os.makedirs(PROCESSED_CSV_DIR)

    clean_data(input_file, output_file)
