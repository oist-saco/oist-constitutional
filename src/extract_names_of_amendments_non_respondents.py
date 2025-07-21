# Takes in the results of the constitutional amendements and a list of 
# peoples emails, returns the mails of all of the people who did not yet answer
# the amendment survey.
# Use fuzzy matching between mails and user ids to accomplish the task

# UNDER CONSTRUCTION

import pandas as pd
from rapidfuzz import process, fuzz

input_folder  = "../confidential_files/"
output_folder = "../confidential_files/"
output_filename = "non_voter_mails.csv"

# Load data
respondents = pd.read_csv(input_folder + "constitutional_amendments_2024_20250707.csv", skiprows=2)
all_people = pd.read_csv(input_folder + "members_info_voters.csv")

# Normalize identifiers
respondents_ids = respondents["Username"].dropna().astype(str).str.lower().str.replace("-", ".")
all_people["Clean email"] = all_people["Email"].dropna().astype(str).str.lower().str.replace("-", ".")
all_people["Username"] = all_people["Clean email"].str.split("@").str[0]

# Get exact matches user and mail
exact_matches = pd.DataFrame()
exact_matches["Username"]    = respondents_ids[respondents_ids.isin(all_people["Username"])] 
exact_matches["Clean email"] = None
for idx, user in exact_matches["Username"].items(): 
  exact_matches.loc[idx,"Clean email"] = all_people["Clean email"][all_people["Username"]==user].values

# Remove them from lists
respondent_ids = respondents_ids.drop(index=exact_matches.index)                        # Respondents that were not exactly matched 
remaining_people  = all_people[~all_people["Username"].isin(exact_matches["Username"])] # All_people minus exactly matched respondents

# Fuzzy matching remaining
fuzzy_matches = []
for resp_number, resp_id in respondent_ids.items():
    match, score, match_number = process.extractOne(
        resp_id.replace(".", " "), remaining_people["Username"].astype(str).str.replace(".", " "), scorer=fuzz.token_set_ratio
    )
    if match is not None:
        fuzzy_matches.append({
            "Respondent index": resp_number,
            "All people index": match_number,
            "Username": resp_id,
            "Respondent": resp_id.replace(".", " "),
            "Matched": match,
            "Clean email": all_people["Clean email"].iloc[match_number],
            "Score": score
        })

# Combine matches
fuzzy_match_df = pd.DataFrame(fuzzy_matches).sort_values(by="Score", ascending=False)
print("\n\n Fuzzy matching results to review:")
print(fuzzy_match_df.to_markdown())
print("\n Manually add the mails that do not match (low scores) to the non-voter list.")

# Obtain all the people that supposedly voted
# In order not to send mails to people that voted, we include all fuzzy matched mails
#  This may mean that some people that did NOT vote will not get an email. Check output of 
#  print(fuzzy_match_df) to make manual changes
people_who_voted = pd.concat([exact_matches, fuzzy_match_df[["Username","Clean email"]]],ignore_index=True)

people_who_did_not_vote = remaining_people[~remaining_people.index.isin(fuzzy_match_df["All people index"])]

# Save results
people_who_did_not_vote["Clean email"].to_csv(output_folder+output_filename, index=False, header=False)
print(f"\n Results saved in: {output_folder+output_filename}\n")

