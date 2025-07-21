import csv
from collections import defaultdict
import os

# Path to base directory of this project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File path for the CSV file containing nominations
nominations_file = os.path.join(base_dir,
    'confidential_files/student_council_officer_nominations_2025_summer_20250705.csv'
)

# Expected positions, mapped to normalized versions for consistency
expected_positions = [
    "Chair",
    "Vice Chair",
    "Secretary",
    "Communications Officer",
    "Diversity Officer",
    "Faculty Assembly Representative",
    "Events Officer",
    #"Academic Officer",
    #"Welfare Officer",
    #"Health and Safety Officer",
    #"Sustainability Representative",
    "IT Officer",
    "Junior Academic Deputy",
    "Senior Academic Deputy",
    "GEDI Representative",
    "Culture and External Relations Representative",
    #"CDC Representative",
    #"Constitutional Officer",
]


def sort_positions(positions):
    # Sort the positions based on the index in the expected_positions list
    return sorted(positions, key=lambda pos: expected_positions.index(pos))


def normalize_columns(header_row):
    normalized_columns = {}
    for column in header_row:
        for position in expected_positions:
            if position.lower() == column.lower().strip():
                normalized_columns[position] = column
    return normalized_columns


nominees = defaultdict(set)
position_counts = defaultdict(int)  # Dictionary to count nominations for each position

with open(nominations_file, "r", encoding="utf-8") as csvfile:

    # Skip first two rows
    for i in range(2):
        next(csvfile)

    reader = csv.DictReader(csvfile, delimiter=",")
    normalized_columns = normalize_columns(reader.fieldnames)

    for row in reader:
        for position, actual_column_name in normalized_columns.items():
            nominee_info = row[actual_column_name].strip() # Extract the nominee information
            if nominee_info:  # Check for non-empty string
                name, email = nominee_info.split("<")
                email = email.strip(">")
                # Only increment count if the position wasn't already added
                if position not in nominees[(name.strip(), email.strip())]:
                    nominees[(name.strip(), email.strip())].add(position)
                    position_counts[position] += 1  # Increment count for the position

# Email drafting parameters
hustings_day = "Friday"
hustings_date = "11th of July"
time = "17:00"
hustings_date_and_time = f"{hustings_date}, {time}"


email_template = """
Dear {name},

Congratulations🎉

You have been **nominated** for the position(s) of **{positions}** of the Student Council.

If you would like to run for this position, **please reply** to this email **by {hustings_date_and_time}** to accept your nomination.

If you’d like to know more about SC affairs, please don’t hesitate to reach out to the current SC officers to ask them questions.

We will hold **Hustings** on {hustings_day}, **{hustings_date_and_time}**. Each nominee is expected to give a **short speech** (max. 2 min) in front of the Student Assembly, expressing why they should be elected, what your experience for the position is, what you want to improve at OIST in the coming year. After all candidates have given their speeches, we will take questions from the current council members and from the Student Assembly. The questions will be unbiased and directed to all candidates running for the same position. The election will take place during the following week.

If you are not available on {hustings_day}, {hustings_date} but still intend to run for the position, please inform the Student Council or me directly ([sutashu.tomonaga@oist.jp](mailto:sutashu.tomonaga@oist.jp)) and let us know.

In addition to the speech, we would like you to **submit a short statement**. Your statement will be published on the Student Assembly website so that students who are unable to attend the Hustings can still have an idea of the candidates' positions. Please send it to me **before the Hustings begin**.


**Note that under the new [ToR](https://groups.oist.jp/sites/default/files/imce/u105953/OIST_SA_Terms_of_Reference_2022.pdf), you may run for two positions!** If you choose to run or think about running for one or two of the positions you were nominated for, please reply to this email.**Not replying will be considered declining**. So, please, only reply if you want to run!


Finally, please carefully read the [Terms of Reference](https://groups.oist.jp/sac/terms-reference) about the position and eligibility for nomination (e.g., the ToR requires a candidate has at least 3 terms remaining in OIST).

If you have any questions, feel free to reach out to me, [studentcouncil@oist.jp](mailto:studentcouncil@oist.jp), ask on Slack, or reach out to any of the [Officers](https://groups.oist.jp/sac/2024-spring-student-council).


Best,

Simone Tandurella

Student Assembly Constitutional Officer (SACO)
"""

# Iterate over nominees and draft emails
for (name, email), positions in nominees.items():
    positions_str = ", ".join(positions)
    email_content = email_template.format(
        name=name.split()[0],
        positions=positions_str,
        hustings_date_and_time=hustings_date_and_time,
        hustings_date=hustings_date,
        hustings_day=hustings_day,
    )
    # print('Draft email for ' + name + ' is:\n' + email_content)

    # Save the draft email to a file
    filename = f"nomination_email_to_{name.replace(' ', '_')}.txt"
    file_path = os.path.join(base_dir, "confidential_files", "email_drafts", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(email_content)
    print(f"Drafted email for {name} saved as {filename}.")


import json


#
def output_nominees_for_power_automate(nominees):
    # Prepare the list of nominees in a format suitable for Power Automate
    nominees_list = []
    for (name, email), positions in nominees.items():
        positions_list = sort_positions(list(positions))

        if len(positions_list) > 2:
            positions_str = (
                ", ".join(positions_list[:-1]) + ", and " + positions_list[-1]
            )  # Removed the trailing comma
        elif len(positions_list) == 2:
            positions_str = positions_list[0] + " and " + positions_list[1]
        else:
            positions_str = positions_list[0] if positions_list else ""

        nominee_data = {
            "Name": name,
            "Email": email,
            "Positions": positions_str,
        }
        nominees_list.append(nominee_data)

    # Output the data as JSON
    # get date label yyyymmdd_hhmm from today using datetime
    import datetime
    today_label = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_file = os.path.join(base_dir, "confidential_files", f"nominees_list_for_power_automate_{today_label}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nominees_list, f, ensure_ascii=False, indent=4)

    print(f"Nominees' Name/Email/Positions JSON saved as {output_file}")

    # Output just the emails for BCC mass emails
    output_email_list = os.path.join(base_dir, "confidential_files", "nominees_emails.txt")
    with open(output_email_list, "w", encoding="utf-8") as f:
        for nominee in nominees_list:
            f.write(nominee["Email"] + "\n")
    print(f"Nominees' Emails saved as {output_email_list}")


# Call the function to output the list
output_nominees_for_power_automate(nominees)

# Output the total nominations for each position
for position, count in position_counts.items():
    print(f"Total nominations for {position}: {count}")

# Sum position count for [    "Vice Chair", "Secretary", "Communications Officer", "Diversity Officer", "Faculty Assembly Representative", "Events Officer",]
total_count_core_officers = sum(
    position_counts[pos]
    for pos in [
        "Chair",
        "Vice Chair",
        "Secretary",
        "Communications Officer",
        "Academic Officer",
        "Welfare Officer",
        "Diversity Officer",
        "Health and Safety Officer",
        "Faculty Assembly Representative",
        "Events Officer",
        "Sustainability Representative"
    ]
)

total_count_associate_officers = sum(
    position_counts[pos]
    for pos in [
        "IT Officer",
        "Senior Academic Deputy",
        "Junior Academic Deputy",
        "GEDI Representative",
        "Culture and External Relations Representative",
        "CDC Representative",
        "Constitutional Officer",
    ]
)

print(f"Total nominations for Core Officers: {total_count_core_officers}")
print(f"Total nominations for Associate Officers: {total_count_associate_officers}")
