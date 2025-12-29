import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup # Keep for debugging suggestion
import os
import re
import warnings
import glob

# Ignore specific pandas/bs4 warnings
warnings.filterwarnings("ignore", "You provided Unicode markup but also provided a value for from_encoding")
warnings.filterwarnings("ignore", "Passing literal html to 'read_html' is deprecated")

# from data_pipeline folder -> data folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_HTML_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'Raw', 'raw_html')
PROCESSED_CSV_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'Processed', 'course_data')

def read_html_content(filepath):
    """Reads HTML content with UTF-8 encoding."""
    # Ensure correct file reading
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  [ERROR] Cannot read file {os.path.basename(filepath)} due to: {e}")
        return None

def print_processing_summary(total_files_found, files_with_data, merged_rows):
    """Prints a summary of the data processing, including the number of files processed."""
    print("\n==============================================")
    print("           Processing Summary")
    print("==============================================")
    print(f"Total HTML files found/processed: {total_files_found}")
    print(f"Files contributing extracted data: {files_with_data}")
    print(f"Total course rows merged:         {merged_rows}")
    print("==============================================")

def convert_html_to_csv():
    
    # Create if it doesn't exists
    if not os.path.exists(PROCESSED_CSV_DIR):
        os.makedirs(PROCESSED_CSV_DIR)
        print(f"Created: {PROCESSED_CSV_DIR}")

    # Find all raw html
    html_files = glob.glob(os.path.join(RAW_HTML_DIR, '*.html'))
    total_files_found = len(html_files) # Total files to iterate over
    
    if not html_files:
        print("not found any HTML files in the raw directory.")
        # Call summary even if empty
        print_processing_summary(0, 0, 0)
        return

    all_data = []
    files_with_data = 0 # Files that successfully contribute > 0 rows
    
    for filepath in html_files:
        filename = os.path.basename(filepath)
        print(f"\n--- Processing: {filename} ---")
        
        html_content = read_html_content(filepath)
        if html_content is None:
            continue

        try:
            # 1. Extract semester and department codes from filename
            parts = filename.split('_')
            # EX: 113S
            ym_code = parts[0]
            # EX: 305305Department... - Heuristic to get the code part before 'Department'
            dept_part = parts[1].split('Department')[0] 
            dept_code = dept_part.split('(')[0].replace('.html', '').replace('.txt', '')
            
            # 2. Robust table extraction using StringIO and multiple parsers (lxml first, then default)
            tables = pd.read_html(StringIO(html_content), flavor='lxml')
            
            if not tables:
                # Retry with default parser if 'lxml' fails
                tables = pd.read_html(StringIO(html_content))
                
            if not tables:
                # Raise error if no tables found
                raise ValueError("No tables found matching pattern '.+'")
                
            # Get the main table (first one found)
            df = tables[0]
            
            # 3. Clean and process the extracted DataFrame
            
            # Add metadata columns
            df['Semester_Code'] = ym_code
            df['Department_Code'] = dept_code
            
            # Set the first row as column headers and remove it
            # Ensure the table is large enough to contain headers and data
            if len(df) > 1:
                df.columns = df.iloc[0]
                df = df[1:].copy()
            else:
                # Skip if the table is too short to contain a header row and data rows
                raise ValueError("Table is too short (<= 1 row) to extract meaningful data.")
            
            # Verify data is valid by dropping rows where the first column (Course ID/No.) is missing
            df = df.dropna(subset=[df.columns[0]]).reset_index(drop=True)

            # Check if any meaningful rows remain after cleaning
            if len(df) > 0:
                print(f"   Extracted {len(df)} rows.")
                all_data.append(df)
                files_with_data += 1 # Increment only on successful data extraction
            else:
                raise ValueError("Table is valid but contains 0 meaningful data rows after cleaning.")

        except ValueError as e:
            # Handle table extraction/cleaning errors
            print(f"   Cannot read {filename}. Reason: {e}")
            
            # Debug suggestion for non-table data
            if re.search(r'<div\s+class=["\'].*row.*["\']', html_content, re.IGNORECASE):
                print("   [DEBUG] Data might be in non-standard <div> layout. Use BeautifulSoup.")

        except Exception as e:
            # Critical error during processing
            print(f"   [CRITICAL ERROR] Failed to process {filename}: {e}")
            
    total_merged_rows = 0
    if all_data:
        # Merge all DataFrames
        # Use an outer join during concatenation to handle inconsistent column names safely
        final_df = pd.concat(all_data, ignore_index=True)
        total_merged_rows = len(final_df)
        
        # Save merged CSV
        output_filepath = os.path.join(PROCESSED_CSV_DIR, 'all_course_listings.csv')
        final_df.to_csv(output_filepath, index=False, encoding='utf-8')
        print(f"\nSuccessfully saved {total_merged_rows} rows into: {output_filepath}")
    else:
        print("\nError: No valid data frames were extracted and merged.")
        
    # Print the summary of all files processed
    print_processing_summary(total_files_found, files_with_data, total_merged_rows)


if __name__ == "__main__":
    convert_html_to_csv()
