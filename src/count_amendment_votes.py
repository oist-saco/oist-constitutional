import csv
import os
from collections import Counter, defaultdict

# Path to base directory of this project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to text file containing web votes
web_file_path = os.path.join(
    base_dir, "confidential_files/constitutional_amendments_2024_20250711.csv"
)

# Path to text file containing paper ballot votes
# IT HAS TO BE PURGED FROM WEBSITE DUPLICATES
ballots_file_path = os.path.join(
    base_dir, "confidential_files/constitutional_amendments_2024_paper_ballots_20250711.csv"
)

# Set the expected number of voters
total_expected_voters = 294

# Initialize counters
response_counts = defaultdict(Counter)
participant_count = 0

# Read the web file
with open(web_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)


# Find the header row (starts with "Serial")
header_row_index = None
for i, row in enumerate(rows):
    if row and row[0].strip() == "Serial":
        header_row_index = i
        break

# Extract headers and relevant columns
headers = rows[header_row_index]
relevant_columns = headers[9:]  # Columns with Accept/Reject responses

# Process each response row
for row in rows[header_row_index + 1:]:
  participant_count += 1
  for i, col in enumerate(relevant_columns, start=9):
      response = row[i].strip()
      if response in ["Accept", "A"]:
          response_counts[col]["Accept"]  += 1
      elif response in ["Reject", "R"]:
          response_counts[col]["Reject"]  += 1
      else:
          response_counts[col]["Abstain"] += 1

# Read the paper file
with open(ballots_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    pb_rows = list(reader)

for amendment_name_web, amendment_name_pb in zip(relevant_columns, pb_rows[0][1:]):
  if amendment_name_web.strip().lower() != amendment_name_pb.strip().lower():
    raise ValueError(f"Amendment identifiers are not the same: {amendment_name_web}, {amendment_name_pb}. \n Please, check the order")

for row in pb_rows[1:]:
    participant_count += 1
    for i, col in enumerate(relevant_columns, start=1):
        response = row[i].strip()
        if response in ["Accept", "A"]:
            response_counts[col]["Accept"]  += 1
        elif response in ["Reject", "R"]:
            response_counts[col]["Reject"]  += 1
        else:
            response_counts[col]["Abstain"] += 1

# Output summary
print(f"\n")
print(f"Total voters: {participant_count}")
print(f"Student Assembly members: {total_expected_voters}")
print(f"Participation rate: {participant_count / total_expected_voters * 100:.2f}%\n")

for col in relevant_columns:
    accept  = response_counts[col]["Accept"]
    reject  = response_counts[col]["Reject"]
    abstain = response_counts[col]["Abstain"]
    total = accept + reject
    accept_pct  = (accept / total * 100) if total > 0 else 0
    reject_pct  = (reject / total * 100) if total > 0 else 0
    abstain_pct = (abstain / total * 100) if total > 0 else 0
    print(f"{col}: Accept = {accept}, Reject = {reject}, Abstain = {abstain}, Accept% = {accept_pct:.2f}%, Reject% = {reject_pct:.2f}%, Abstain% = {abstain_pct:.2f}%,")

