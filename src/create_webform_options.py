import csv
import re

def sanitize(input_string):
    """Sanitize the input string to be used as a safe key."""
    return re.sub(r'\W+', '_', input_string).lower()

def create_webform_options(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        options = []

        for row in reader:
            if row['Position'] == 'OIST Student':
                safe_key = sanitize(row['Name'])
                readable_option = f"{row['Name']} <{row['Email']}>"
                options.append(f"{safe_key}|{readable_option}")

        # Sort the options list alphabetically by the readable part (after the safe key)
        options.sort(key=lambda x: x.split('|')[1])

    with open(output_file, 'w', encoding='utf-8') as file:
        for option in options:
            file.write(option + '\n')

    print(f"Options successfully saved to {output_file}.")

# Specify the input and output file paths
input_csv_file = '../confidential_files/members_info.csv'
output_txt_file = '../confidential_files/webform_options.txt'

# Generate the options file
create_webform_options(input_csv_file, output_txt_file)
