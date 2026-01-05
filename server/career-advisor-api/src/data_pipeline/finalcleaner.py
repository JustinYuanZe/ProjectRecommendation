import pandas as pd
import os
import re

def clean_course_data():
    """
    Clean course data to keep English course names, teaching in English flag, AND course codes
    """
    
    # Get the correct file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define file paths
    input_file = os.path.join(project_root, "data", "Processed", "course_data", "cleaned_course_data.csv")
    output_file = os.path.join(project_root, "data", "Processed", "course_data", "final_cleaned_courses.csv")
    
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        print(f"📊 Original data shape: {df.shape}")
        
        # Create cleaned data with ALL necessary information for mapping
        cleaned_data = []
        
        for index, row in df.iterrows():
            course_title_en = str(row['Course_Title_EN']).strip() if pd.notna(row['Course_Title_EN']) else ""
            course_code = str(row['Course_Code']).strip() if pd.notna(row['Course_Code']) else ""
            section = str(row['Section']).strip() if pd.notna(row['Section']) else ""
            
            # If English title is empty, create meaningful placeholder
            if not course_title_en or course_title_en == 'nan':
                chinese_title = str(row['Course_Title_CN']).strip() if pd.notna(row['Course_Title_CN']) else ""
                if chinese_title and chinese_title != 'nan':
                    course_title_en = f"[Chinese] {chinese_title}"
                else:
                    course_title_en = f"Course_{course_code}_{section}"
            
            # Check if course is taught in English
            teaching_in_english = False
            for col in df.columns:
                if pd.notna(row[col]) and 'Teaching in English' in str(row[col]):
                    teaching_in_english = True
                    break
            
            # Clean the course name (but keep original for reference)
            course_title_clean = re.sub(r'\*Teaching in English\*', '', course_title_en)
            course_title_clean = re.sub(r'\s*\*\s*', ' ', course_title_clean).strip()
            course_title_clean = re.sub(r'\s+', ' ', course_title_clean)
            
            # Add to cleaned data - KEEP ALL MAPPING INFORMATION
            cleaned_data.append({
                'Course_Code': course_code,
                'Section': section,
                'Course_Name_EN': course_title_clean,
                'Original_Course_Name': course_title_en,  # Keep original for reference
                'Teaching_in_English': teaching_in_english,
                'Program_Year': row['Program_and_Year'] if pd.notna(row['Program_and_Year']) else '',
                'Course_Type': row['Course_Type'] if pd.notna(row['Course_Type']) else '',
                'Instructor_EN': row['Instructor_EN'] if pd.notna(row['Instructor_EN']) else '',
                'Original_Index': index  # Keep for debugging
            })
        
        # Create final dataframe
        final_df = pd.DataFrame(cleaned_data)
        
        print(f"📊 After processing: {len(final_df)} rows")
        print(f"🌍 Courses taught in English: {final_df['Teaching_in_English'].sum()}")
        print(f"🔑 Unique course codes: {final_df['Course_Code'].nunique()}")
        
        # Save the data
        try:
            final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"💾 Output saved to: {output_file}")
        except PermissionError:
            alt_output_file = os.path.join(project_root, "data", "Processed", "course_data", "courses_with_codes.csv")
            print(f"⚠️  Permission denied, using alternative: {alt_output_file}")
            final_df.to_csv(alt_output_file, index=False, encoding='utf-8-sig')
            output_file = alt_output_file
        
        # Display statistics
        print(f"\n📈 Detailed Statistics:")
        print(f"   Total course entries: {len(final_df)}")
        print(f"   Unique course codes: {final_df['Course_Code'].nunique()}")
        print(f"   English-taught courses: {final_df['Teaching_in_English'].sum()} ({final_df['Teaching_in_English'].sum()/len(final_df)*100:.1f}%)")
        
        # Show sample with course codes
        print(f"\n🔍 Sample data (with course codes):")
        print(final_df[['Course_Code', 'Section', 'Course_Name_EN', 'Teaching_in_English']].head(10))
        
        return final_df
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def create_mapping_summary():
    """
    Create a mapping summary for easy reference
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    input_file = os.path.join(project_root, "data", "Processed", "course_data", "cleaned_course_data.csv")
    output_file = os.path.join(project_root, "data", "Processed", "course_data", "course_mapping_summary.csv")
    
    try:
        df = pd.read_csv(input_file)
        
        # Create mapping summary (one row per unique course code)
        mapping_data = []
        
        for course_code in df['Course_Code'].unique():
            if pd.notna(course_code):
                course_rows = df[df['Course_Code'] == course_code]
                first_row = course_rows.iloc[0]
                
                course_title_en = str(first_row['Course_Title_EN']).strip() if pd.notna(first_row['Course_Title_EN']) else ""
                
                # Clean course name
                if course_title_en and course_title_en != 'nan':
                    course_clean = re.sub(r'\*Teaching in English\*', '', course_title_en)
                    course_clean = re.sub(r'\s*\*\s*', ' ', course_clean).strip()
                    course_clean = re.sub(r'\s+', ' ', course_clean)
                else:
                    course_clean = f"Course_{course_code}"
                
                # Check if any section is taught in English
                teaching_english = any(
                    any('Teaching in English' in str(row[col]) for col in df.columns if pd.notna(row[col]))
                    for _, row in course_rows.iterrows()
                )
                
                mapping_data.append({
                    'Course_Code': course_code,
                    'Course_Name': course_clean,
                    'Taught_in_English': teaching_english,
                    'Total_Sections': len(course_rows),
                    'Sections': ', '.join([str(s) for s in course_rows['Section'].unique() if pd.notna(s)])
                })
        
        mapping_df = pd.DataFrame(mapping_data).sort_values('Course_Code')
        
        print(f"\n📋 Mapping Summary:")
        print(f"   Unique course codes: {len(mapping_df)}")
        print(f"   English-taught courses: {mapping_df['Taught_in_English'].sum()}")
        
        mapping_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"💾 Mapping summary saved to: {output_file}")
        
        return mapping_df
        
    except Exception as e:
        print(f"❌ Error in mapping summary: {e}")
        return None

if __name__ == "__main__":
    print("Starting final cleaning process...")
    print("=" * 60)
    
    # Create main version with ALL course entries (for detailed mapping)
    all_courses = clean_course_data()
    
    # Create mapping summary (for quick lookup)
    mapping_summary = create_mapping_summary()
    
    if all_courses is not None:
        print("\n" + "=" * 60)
        print("✅ Cleaning process completed successfully!")
        print("=" * 60)
        print(f"📁 Main file: {len(all_courses)} course entries")
        print(f"📁 Mapping summary: {len(mapping_summary) if mapping_summary is not None else 0} unique courses")
        print(f"🔑 Course codes preserved for user mapping!")
    else:
        print("\n" + "=" * 60)
        print("❌ Cleaning process failed!")
        print("=" * 60)