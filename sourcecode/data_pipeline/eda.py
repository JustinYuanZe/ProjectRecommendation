import pandas as pd
import os

# --- Setup File Paths ---
# Assuming the script runs from a folder like 'data_pipeline' 
# and the CSV is in '../data/Processed/course_data'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_CSV_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'Processed', 'course_data')

input_file = os.path.join(PROCESSED_CSV_DIR, 'cleaned_course_data.csv')

def run_eda(filepath):
    """
    Performs exploratory data analysis (EDA) on the cleaned dataset.
    """
    print("--- Starting Exploratory Data Analysis (EDA) ---")
    print(f"Loading data from: {filepath}\n")
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {filepath}. Please ensure 'cleaned_course_data.csv' exists.")
        return

    # 1. Data Structure Overview
    print("## 1. Data Structure Overview")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print("\n--- Column Data Types and Non-Null Counts ---")
    df.info()

    # 2. Missing Data Analysis
    print("\n## 2. Missing Data Analysis (in %)")
    missing_data = df.isnull().sum() * 100 / len(df)
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
    if not missing_data.empty:
        print(missing_data.to_string(float_format="%.2f%%"))
    else:
        print("No missing values found in the dataset! Great job cleaning.")

    # 3. Course and Department Statistics
    print("\n## 3. Course and Department Statistics")
    
    # Count the number of unique courses
    unique_courses = df['Course_Code'].nunique()
    print(f"Total Unique Course Codes: {unique_courses}")
    
    # Analyze Departments
    if 'Department_ID_Name' in df.columns:
        unique_departments = df['Department_ID_Name'].nunique()
        print(f"Total Unique Departments: {unique_departments}")
        
        print("\n--- Top 10 Departments by Course Count ---")
        top_departments = df['Department_ID_Name'].value_counts().head(10)
        print(top_departments.to_string())
        
    # Analyze course types
    if 'Course_Type' in df.columns:
        print("\n--- Course Type Distribution ---")
        course_type_counts = df['Course_Type'].value_counts()
        print(course_type_counts.to_string())
        
    # Analyze Credits (Assuming credits were separated after the parser step, 
    # but we can still analyze the raw column if needed)
    if 'Schedule_and_Credits_Raw' in df.columns:
         print("\n--- Schedule and Credits Raw Sample ---")
         print(df['Schedule_and_Credits_Raw'].value_counts().head(5).to_string())


if __name__ == "__main__":
    # Ensure the directory exists before attempting to save the file
    if not os.path.exists(PROCESSED_CSV_DIR):
        print(f"Creating directory: {PROCESSED_CSV_DIR}")
        os.makedirs(PROCESSED_CSV_DIR)

    run_eda(input_file)
