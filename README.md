# oist-constitutional

## src
For scripts.
Contains:
### `voting_results.py`
- Counts votes for SC elections 
- Usage: python voting_results.py <csv_file> <log_file> <out_path>
- Original author: Stefano Pascarelli, Jan 30 2020
### `extract_name_and_info.py`
- Extracts the html from People Directory `https://directory.oist.jp/`
### `create_webform_options.py`
- Creates a option list for Groups Webform in the format `safe_key|Some readable option`
- Copy and paste the contents of the generated text file into the Options in the webform option.
