import pandas as pd
import numpy as np
import os
import re

# from data_pipeline folder -> data folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'Processed', 'course_data')
RAW_LISTINGS_FILE = os.path.join(PROCESSED_DATA_DIR, 'all_course_listings.csv')
CLEANED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, 'cleaned_course_data.csv')

def load_data(filepath):
    """Loads the raw combined CSV data."""
    if not os.path.exists(filepath):
        print(f"Error: Raw data file not found at {filepath}")
        return None
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def clean_and_transform_data(df):
    """Performs cleaning and transformation steps on the DataFrame."""
    
    # 1. Identify and remove columns that are entirely NaN after merging
    original_cols = df.columns
    df.dropna(axis=1, how='all', inplace=True)
    if len(df.columns) < len(original_cols):
        print("Dropped empty columns. Dataset width reduced.")

    # Standardize column names based on the structure observed in the raw data sample
    # We map the first 9 positions to meaningful names.
    CLEANED_COLUMNS = [
        'Department_Year_Raw',        # Ex: "International Language and Culture Center(Master Program), Second Year"
        'Course_ID',                  # Ex: EL228
        'Class_Section',              # Ex: D
        'Course_Title_Raw_CN',        # Ex: 口語英文溝通
        'Course_Title_Raw_EN',        # Ex: Oral English Communication *Teaching in English *寰宇文化微學程
        'Credit_Hours',               # Ex: 2 or Department Elective Courses
        'Teacher_Name_CN',            # Ex: 文天瑞
        'Teacher_Name_EN',            # Ex: WALTER TREY DOMINIC HAIRSTON
        'Class_Time_Location_Raw'     # Ex: 506 ,1111 507 ,1111 (We will keep this raw)
    ]
    
    current_cols = df.columns.tolist()
    
    # Apply the renaming for the first 9 known columns
    rename_dict = {}
    for i, new_name in enumerate(CLEANED_COLUMNS):
        if i < len(current_cols):
            rename_dict[current_cols[i]] = new_name
        else:
            break
    
    df.rename(columns=rename_dict, inplace=True)
    
    # --- Data Cleaning Specifics ---

    # 2. Remove noisy rows (Selection message)
    initial_rows = len(df)
    
    # The 'Selection message' junk seems to be in the 'Credit_Hours' column
    junk_col = 'Credit_Hours'
    
    if junk_col in df.columns:
        # Filter out rows containing the known noise text
        df_cleaned = df[~df[junk_col].astype(str).str.contains('Selection message', case=False, na=False)].copy()
        removed_rows = initial_rows - len(df_cleaned)
        print(f"Removed {removed_rows} noisy 'Selection message' rows.")
        df = df_cleaned
    else:
        print("Warning: Junk column not found. Skipping 'Selection message' removal.")

    # 3. Separate Course Titles and Extract Notes
    if 'Course_Title_Raw_CN' in df.columns and 'Course_Title_Raw_EN' in df.columns:
        
        df.rename(columns={'Course_Title_Raw_CN': 'Course_Title_CN', 
                           'Course_Title_Raw_EN': 'Course_Title_EN'}, inplace=True)
        
        # Extract notes (e.g., *Teaching in English) into a dedicated column
        # Regex captures everything starting with an asterisk (*)
        df['Course_Notes'] = df['Course_Title_EN'].str.extract(r'(\*.*)').fillna('').str.strip()
        
        # Remove the notes from the English Title
        df['Course_Title_EN'] = df['Course_Title_EN'].str.replace(r'\*.*', '', regex=True).str.strip()
    
    # 4. Extract Semester Code and Department/Program Name from Department_Year_Raw
    if 'Department_Year_Raw' in df.columns:
        # Example: "International Language and Culture Center(Master Program), Second Year"
        
        # Capture everything before the comma as Department_Program_Raw
        df['Department_Program_Raw'] = df['Department_Year_Raw'].str.split(',', n=1).str[0].str.strip()
        
        # Capture the year/semester info after the comma as Semester_Info_Raw
        df['Semester_Info_Raw'] = df['Department_Year_Raw'].str.split(',', n=1).str[1].str.strip()
        
        # Assuming the semester info is the last word(s)
        # Example: "Second Year"
        df['Academic_Year'] = df['Semester_Info_Raw'].str.extract(r'(\w+ Year|\w+)\s*$').fillna('').str.strip()
        
        df.drop(columns=['Department_Year_Raw', 'Semester_Info_Raw'], inplace=True, errors='ignore')

    # 5. Final selection of columns and cleaning
    
    # Define the final set of columns to keep (excluding complex time/location columns)
    final_cols_to_keep = [
        'Course_ID', 'Class_Section', 'Course_Title_CN', 'Course_Title_EN', 
        'Credit_Hours', 'Teacher_Name_CN', 'Teacher_Name_EN', 'Course_Notes',
        'Department_Program_Raw', 'Academic_Year', 'Class_Time_Location_Raw' # Keeping raw location data
    ]
    
    # Filter to only keep columns that actually exist after all transformations
    existing_final_cols = [col for col in final_cols_to_keep if col in df.columns]
    
    # Drop rows where the primary key (Course_ID) is null
    if 'Course_ID' in df.columns:
        df.dropna(subset=['Course_ID'], inplace=True)
        
    # Drop rows where both Chinese and English titles are missing
    df.dropna(subset=['Course_Title_CN', 'Course_Title_EN'], how='all', inplace=True)

    # Return the final cleaned DataFrame with only the relevant columns
    return df[existing_final_cols]

def main():
    """Main function to run the cleaning process."""
    print("--- Starting Data Cleaning Process ---")
    
    df = load_data(RAW_LISTINGS_FILE)
    if df is None:
        return
    
    print(f"Loading raw data from: {RAW_LISTINGS_FILE}")
    print(f"Total rows before cleaning: {len(df)}")
    
    cleaned_df = clean_and_transform_data(df)
    
    if cleaned_df is not None:
        # Save the final cleaned CSV
        cleaned_df.to_csv(CLEANED_DATA_FILE, index=False, encoding='utf-8')
        print(f"Total structured rows saved: {len(cleaned_df)}")
        print(f"Successfully saved cleaned data to: {CLEANED_DATA_FILE}")

if __name__ == "__main__":
    main()
