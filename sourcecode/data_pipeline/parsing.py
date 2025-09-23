from bs4 import BeautifulSoup
import pandas as pd


def ParseTheTable(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table', {'id': 'Table1'})

    if not table:
        print("not found")
        return []
    
    rows = table.find_all('tr')
    courses_data = []

    for i in range(1, len(rows), 2):
        try:
            course_row = rows[i]
            message_row = rows[i+1]

            cells = course_row.find_all('td')

            if len(cells) < 7:
                continue
            
            course_id_class = cells[1].get_text(strip=True)
            department_year = cells[2].get_text(strip=True)
            course_name_cell = cells[3]
            course_name_text = cells[3].get_text(strip=True, separator='\n')
            course_name_parts = course_name_text.split('\n')
            
            chinese_name = course_name_parts[0].replace('(Syllabus)', '').strip()
            br_tag = course_name_cell.find('br')
            if br_tag and br_tag.next_sibling:
                english_name = br_tag.next_sibling.strip()
                if english_name.startswith('*'):
                     english_name = ''
            else:
                english_name = ''


            is_english_taught = False
            english_tag = course_name_cell.find('font', {'color': 'blue'})
            if english_tag and "*Teaching in English" in english_tag.get_text():
                is_english_taught = True

            if 'Teaching in English' in english_name:
                second_br = course_name_cell.find_all('br')[1]
                if second_br and second_br.next_sibling:
                    english_name = second_br.next_sibling.strip()


            course_info = {
                'Course ID and Class': course_id_class,
                'Department & Year Available': department_year,
                'Chinese Course Name': chinese_name,
                'English Course Name': english_name,
                'Is Taught in English': is_english_taught
            }
            courses_data.append(course_info)

        except (IndexError, AttributeError):
            continue
            
    return courses_data

if __name__ == '__main__':
    with open('raw_table.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    parsed_data = ParseTheTable(html_content)
    if parsed_data:
        print("Successful")
        print(parsed_data[0])
    else:
        print("Failed at Parsing")