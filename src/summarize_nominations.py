import csv
from collections import defaultdict
import os

# Path to base directory of this project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the nominations from the webform
def load_nominations(nominations_file):
    nominations = defaultdict(list)  # Key: Name, Value: list of positions nominated for
    with open(nominations_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            for position in ['Vice Chair', 'Secretary', 'Communications Officer', 'Diversity Officer', 'Faculty Assembly Representative', 'Events Officer', 'IT Representative', 'Senior Academic Deputy', 'Junior Academic Deputy', 'GEDI Representative', 'Culture and External Relations Officer', 'CDC Representative', 'Academic Officer']:
                # Check if the position exists in the row
                print(row)
                if row[position]: # Check if the position has a nominee
                    nominations[row[position]].append(position)
    print(nominations)
    return nominations

# Load member information
def load_members_info(members_info_file):
    members_info = {}  # Key: Name, Value: (Email, Position)
    with open(members_info_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')  # specify the delimiter as '\t'
        for row in reader:
            print(row)
            members_info[row['Name']] = (row['Email'], row['Position'])
    return members_info

# Match nominations with member info
def match_nominations_with_members(nominations, members_info):
    official_nominees = []  # List of tuples: (Name, Email, Nominated Positions, Position)
    for nominee, positions in nominations.items():
        if nominee in members_info:
            email, position = members_info[nominee]
            official_nominees.append((nominee, email, positions, position))
    return official_nominees

# Main function to tie everything together
def main(nominations_file, members_info_file):
    nominations = load_nominations(nominations_file)
    members_info = load_members_info(members_info_file)
    official_nominees = match_nominations_with_members(nominations, members_info)

    # Printing the result for demonstration
    for nominee in official_nominees:
        print(f"Name: {nominee[0]}, Email: {nominee[1]}, Nominated for: {', '.join(nominee[2])}, Position: {nominee[3]}")

# Example usage
if __name__ == "__main__":
    nomination_results_downloaded_file = os.path.join(base_dir, 'confidential_files/nomination_results.csv')
    nominated_members_info_file = os.path.join(base_dir, 'confidential_files/extracted_members_info.csv')
    main(nomination_results_downloaded_file, nominated_members_info_file)
