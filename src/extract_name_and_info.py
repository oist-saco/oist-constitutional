from bs4 import BeautifulSoup
import csv

# Path to your file
file_path = '../confidential_files/people_dir_html_20250514.txt'

# Read the HTML content from the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all person details wrappers
people = soup.find_all("div", class_="oist-pl-teaser__wrapper oist-pl-department__teaser__wrapper")

# Associating positions names with a string to use for separating output
positions_dict = { 'phds'    : {'OIST Student', 'Junior Research Fellow'}
                  ,'interns' : {'Research Intern'}
                  ,'srs'     : {'Visiting Research Student','Special Research Student'}
                  ,'others'  : set()
                 }

# Listing all positions defined
known_positions = set()
for pos_set in positions_dict.values():
    known_positions.update(pos_set)

# Prepare a list to hold the extracted information
members_info = []

# Iterate through each person and extract the relevant information
for person in people:
    name = person.find("div", class_="oist-pl-department__person-name-en")
    
    # Extracting the position name
    position = person.find("div", class_="oist-pl-department__position__name-en")
    if position is None:
        position_text = ""  # In case there is no position found
    else:
        position_text = position.text.strip()

    # If position is not among the declared ones still keep track of it
    if position_text not in known_positions:
        positions_dict['others'].add(position_text)
    
    # Correcting the email extraction by specifically looking for the mailto link
    email_link = person.find("a", href=lambda href: href and "mailto:" in href)
    
    if name and email_link:

        member = {}

        # Extract the text for the name and the email address from the 'href' attribute
        member['name'] = name.text.strip()
        member['email'] = email_link['href'].replace("mailto:", "").strip()

        member['position'] = position_text
        
        # Add the extracted information to our list (now including the position)
        members_info.append(member)


# Add a group including everyone
everyone = set()
for positions in positions_dict.values():
    everyone.update(positions)
positions_dict['everyone'] = everyone


# Get a unique output filename for each group
def make_output_file_path(group
                         ,filepath_prefix='../confidential_files/members_info'
                         ,filepath_suffix='.csv'
                         ,sep='_'
                          ):
    if group == '':
        sep = ''

    return filepath_prefix + sep + group + filepath_suffix


def write_group_members_to_file(filepath, group):
    
  # Writing to the CSV file
  with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      # Write the header row
      writer.writerow(['Name', 'Email', 'Position'])
      # Write the member information if they belong to the specified group
      for member in members_info:
          if member['position'] in positions_dict[group]: 
              writer.writerow(member.values())

  print(f"Information about {group} successfully saved to {output_file_path}.")




# Iterate over all groups we want to split output into
for group in positions_dict.keys():
  
  # Specify the file you want to write to
  output_file_path = make_output_file_path(group)

  # Write a file for each group
  write_group_members_to_file(output_file_path, group)

