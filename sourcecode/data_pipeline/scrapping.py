import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

#Entry URL:
ENTRY_URL= "https://portalfun.yzu.edu.tw/cosSelect/index.aspx?D=G"
#It's enough to scrape last year spring and fall semester:
TARGET_YMS = ["113,2","113,1"]
#Save to raw_html folder, I assume that the script is run from the 'data_pipeline':

##Full directory of this script which works universally:
FULLPATH_DIR=os.path.abspath(__file__)
##Track at the folder of this script("data_pipeline"):
SCRIPT_DIR=os.path.dirname(FULLPATH_DIR)
##moving back [..]("career-advisor-ai")<-[..]("sourcecode")<-[SCRIPT_DIR]("data_pipeline") then ->data->Raw->raw_html
RAW_HTML_DIR=os.path.join(SCRIPT_DIR,'..','..','data','Raw','raw_html')

#I wanna convert 1132 to S,1131 to F:
def get_semester_code(ym_value):
    if "113,2" in ym_value:
        return "S"
    elif "113,1" in ym_value:
        return "F"
    return "X"

def scrape_and_save_to_html():
    #Create the raw HTML directory if it doesn't exist
    if not os.path.exists(RAW_HTML_DIR):
        os.makedirs(RAW_HTML_DIR)
    #Set up the Chrome WebDriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)
    try:
        #Go to the entry page and click the English link once started
        driver.get(ENTRY_URL)
        print("clicking english ver")
        english_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="Index.aspx?Lang=EN"]')))
        english_link.click()
        # delay
        time.sleep(2)
        #Wait for the dropdowns(DDL_YM,DDL_Dept)
        ddl_ym_element = wait.until(EC.presence_of_element_located((By.ID, "DDL_YM")))
        ddl_dept_element = wait.until(EC.presence_of_element_located((By.ID, "DDL_Dept")))
        
        #Convert to the selenium object
        ddl_dept = Select(ddl_dept_element)
        #mapping codes to names
        dept_map = {option.get_attribute("value").strip(): option.text.strip() for option in ddl_dept.options}
        dept_values = list(dept_map.keys())

        #Loop through 113,2 and 113,1:
        for ym_val in TARGET_YMS:
            for dept_val in dept_values:
                print(f"Scraping for YM: {ym_val}, Dept: {dept_val}")


                try:
                    # Re-locate the DDL_YM dropdown
                    ddl_ym = Select(wait.until(EC.presence_of_element_located((By.ID, "DDL_YM"))))
                    
                    # Find the option with the correct stripped value
                    found_ym_option = None
                    for option in ddl_ym.options:
                        if option.get_attribute("value").strip() == ym_val:
                            found_ym_option = option
                            break
                    
                    if found_ym_option:
                        #use the original, non-stripped value to select the option
                        ddl_ym.select_by_value(found_ym_option.get_attribute("value"))
                    else:
                        print(f"Option '{ym_val}' not available. Skipping.")
                        continue

                    # The DDL_Dept will postback and reload. Wait...
                    wait.until(EC.visibility_of_element_located((By.ID, "DDL_Dept")))
                    ddl_dept = Select(driver.find_element(By.ID, "DDL_Dept"))
                    if dept_val in [option.get_attribute("value").strip() for option in ddl_dept.options]:
                        ddl_dept.select_by_value(dept_val)
                    else:
                        print(f"Department '{dept_val}' not available for this combination. Skipping.")
                        continue

                    #The DDL_Degree will update after the department selection.
                    #wait for the DDL_Degree options to load
                    ddl_degree_element = wait.until(EC.element_to_be_clickable((By.ID, "DDL_Degree")))
                    ddl_degree = Select(ddl_degree_element)
                    degree_map = {option.get_attribute("value").strip(): option.text.strip() for option in ddl_degree.options}
                    degree_values = list(degree_map.keys())

                    for degree_val in degree_values:
                        # Skip the "All"
                        if degree_map.get(degree_val) == "All":
                            print(f"  > Skipping 'All' degree option.")
                            continue

                        print(f"  > Degree: {degree_val}")
                        
                        # Re-locate the degree dropdown before selecting
                        ddl_degree = Select(wait.until(EC.element_to_be_clickable((By.ID, "DDL_Degree"))))
                        
                        if degree_val in [option.get_attribute("value").strip() for option in ddl_degree.options]:
                            ddl_degree.select_by_value(degree_val)
                        else:
                            print(f"  > Degree '{degree_val}' not available. Skipping.")
                            continue

                        #click the Inquery button
                        inquery_button = wait.until(EC.element_to_be_clickable((By.ID, "Button1")))
                        inquery_button.click()
                        
                        #wait for the table
                        table_element = wait.until(EC.presence_of_element_located((By.ID, "Table1")))

                        #only take table
                        table_content = table_element.get_attribute("outerHTML")
                        
                        #construct file name
                        ym_prefix = ym_val.split(',')[0]
                        semester_code = get_semester_code(ym_val)
                        
                        dept_name = dept_map.get(dept_val, "Unknown_Dept")
                        degree_name = degree_map.get(degree_val, "Unknown_Degree")

                        sanitized_dept_name = dept_name.replace(" ", "").replace("/", "")
                        sanitized_degree_name = degree_name.replace(" ", "").replace("/", "")
                        
                        filename = f"{ym_prefix}{semester_code}_{dept_val}{sanitized_dept_name}{sanitized_degree_name}.html"
                        filepath = os.path.join(RAW_HTML_DIR, filename)

                        # Save the HTML to the specified file path
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(table_content)
                        
                        print(f"Saved HTML to {filepath}")

                        # Go back to the previous page to continue the loop
                        driver.back()
                        # Wait for the main page to load again before the next selection
                        wait.until(EC.presence_of_element_located((By.ID, "DDL_YM")))
                except Exception as e:
                    print(f"An error occurred while scraping: {e}")
                    # Go back to the main page to reset the state if error
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.ID, "DDL_YM")))
                    continue
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_and_save_to_html()


