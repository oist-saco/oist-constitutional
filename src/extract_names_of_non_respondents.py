# Takes in the results of the constitutional amendements and a list of 
# peoples emails, returns the mails of all of the people who did not yet answer
# the amendment survey.
# Use fuzzy matching between mails and user ids to accomplish the task

# UNDER CONSTRUCTION

import pandas as pd
from rapidfuzz import process, fuzz

input_folder = "../confidential_files/"

# Load CSVs
respondents = pd.read_csv(input_folder + "constitutional_amendments_2024_20250514.csv", skiprows=2)
all_people = pd.read_csv(input_folder + "members_info_phds.csv")

# Columns with strings, cleaned and normalized
respondentsID = respondents["Username"].dropna().astype(str).str.lower().str.replace("-", ".")
all_peopleID = all_people["Email"].dropna().astype(str).str.lower()
all_peopleID = all_peopleID.str.split("@").str[0]

# Step 1: Exact match first
exact_matches = []
exact_matched_all_peopleID_indices = set()
exact_matched_respondentsID_indices = set()

for idx, respID in respondentsID.items():
    exact_match_indices = all_peopleID[all_peopleID == respID].index.tolist()
    if exact_match_indices:
        match_idx = exact_match_indices[0]
        exact_matches.append({
            "Index1": idx,
            "Original": respID,
            "Matched": respID,
            "Match Index": match_idx,
            "Original Email": all_peopleID.loc[match_idx],
            "Score": 100
        })
        exact_matched_all_peopleID_indices.add(match_idx)
        exact_matched_respondentsID_indices.add(idx1)

# Remove exact matches before fuzzy search
respondentsID_remaining = respondentsID.drop(index=exact_matched_respondentsID_indices)
all_peopleID_remaining = all_peopleID.drop(index=exact_matched_all_peopleID_indices)
all_peopleID_remaining = all_peopleID.drop(index=exact_matched_all_peopleID_indices)

# Step 2: Fuzzy match
fuzzy_matches = []
fuzzy_matched_indices = set()

for idx1, val1 in respondentsID_remaining.items():
    match_val, score, match_idx = process.extractOne(
        val1,
        all_peopleID_cleaned_remaining,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=0
    )

    if match_val is not None:
        fuzzy_matched_indices.add(match_idx)
        fuzzy_matches.append({
            "Index1": idx1,
            "Original": val1,
            "Matched": match_val,
            "Match Index": match_idx,
            "Original Email": all_peopleID_remaining.loc[match_idx],
            "Score": score
        })

# Combine all matches and sort by descending score
all_matches = exact_matches + fuzzy_matches
matches_df = pd.DataFrame(all_matches).sort_values(by="Score", ascending=False)

# DataFrame of unmatched rows from original all_peopleID
all_matched_indices = exact_matched_all_peopleID_indices.union(fuzzy_matched_indices)
unmatched_df = all_peopleID.drop(index=all_matched_indices).reset_index(drop=True)

# Save both
matches_df.to_csv("fuzzy_matches.csv", index=False)
unmatched_df.to_csv("unmatched_entries.csv", index=False)

# Preview results
print("Top Matches:\n", matches_df.head())
print("\nUnmatched Rows in all_peopleID:\n", unmatched_df.head())


import pandas as pd
from rapidfuzz import process, fuzz

# Load data
input_folder = "../confidential_files/"
respondents = pd.read_csv(input_folder + "constitutional_amendments_2024_20250514.csv", skiprows=2)
all_people = pd.read_csv(input_folder + "members_info_phds.csv")

# Normalize identifiers
respondents_ids = respondents["Username"].dropna().astype(str).str.lower().str.replace("-", ".")
all_emails = all_people["Email"].dropna().astype(str).str.lower()
all_ids = all_emails.str.split("@").str[0]

# Exact matches
exact_matches = respondents_ids[respondents_ids.isin(all_ids)]
exact_indices = all_ids[all_ids.isin(exact_matches)].index
respondents_exact_indices = respondents_ids[respondents_ids.isin(all_ids)].index

# Prepare for fuzzy matching
remaining_respondents = respondents_ids.drop(index=respondents_exact_indices)
remaining_ids = all_ids.drop(index=exact_indices)

# Fuzzy matching
fuzzy_matches = []
for idx, resp_id in remaining_respondents.items():
    match, score, match_idx = process.extractOne(
        resp_id, remaining_ids, scorer=fuzz.token_sort_ratio
    )
    if match:
        fuzzy_matches.append({
            "Respondent Index": idx,
            "Original": resp_id,
            "Matched": match,
            "Email": all_emails.iloc[match_idx],
            "Score": score
        })

# Combine matches
exact_match_df = pd.DataFrame({
    "Original": exact_matches,
    "Matched": exact_matches,
    "Email": all_emails.loc[exact_indices].values,
    "Score": 100
})
fuzzy_match_df = pd.DataFrame(fuzzy_matches)
matches_df = pd.concat([exact_match_df, fuzzy_match_df], ignore_index=True).sort_values(by="Score", ascending=False)

# Unmatched emails
matched_indices = set(exact_indices).union(fuzzy_match_df["Email"].index if not fuzzy_match_df.empty else [])
unmatched_df = all_emails.drop(index=matched_indices).reset_index(drop=True)

# Save results
matches_df.to_csv("fuzzy_matches.csv", index=False)
unmatched_df.to_csv("unmatched_entries.csv", index=False)

# Preview
print("Top Matches:\n", matches_df.head())
print("\nUnmatched Emails:\n", unmatched_df.head())


