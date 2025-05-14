# Takes in the results of the constitutional amendements and a list of 
# peoples emails, returns the mails of all of the people who did not yet answer
# the amendment survey.
# Use fuzzy matching between mails and user ids to accomplish the task

# UNDER CONSTRUCTION

import pandas as pd
from rapidfuzz import process, fuzz

# Load CSVs
df1 = pd.read_csv("file1.csv")
df2 = pd.read_csv("file2.csv")

# Columns with strings
series1 = df1["NameA"].dropna().astype(str)
series2 = df2["NameB"].dropna().astype(str)

# Preprocess: Strip domain part from email-like entries in series2
series2_cleaned = series2.str.split("@").str[0]

# Keep track of match indices
matched_indices = set()
matches = []

# Match each entry in series1 to the best entry in series2_cleaned
for idx1, val1 in series1.items():
    match_val, score, match_idx = process.extractOne(
        val1,
        series2_cleaned,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=0  # You can increase this if needed
    )
    
    if match_val is not None:
        matched_indices.add(match_idx)
        matches.append({
            "Index1": idx1,
            "Original": val1,
            "Matched": match_val,
            "Match Index": match_idx,
            "Original Email": series2.loc[match_idx],
            "Score": score
        })

# Create DataFrame of matches
matches_df = pd.DataFrame(matches)

# DataFrame of unmatched rows from original series2
unmatched_df = series2.drop(index=matched_indices).reset_index(drop=True)

# Optional: Save both
matches_df.to_csv("fuzzy_matches.csv", index=False)
unmatched_df.to_csv("unmatched_entries.csv", index=False)

# Preview results
print("Top Matches:\n", matches_df.head())
print("\nUnmatched Rows in series2:\n", unmatched_df.head())

