import os
import pandas as pd

import json


data_folder = os.path.join(os.path.dirname(__file__), "data", "outreach_extract")

data_filename = "Outreach Requests.xlsx"


requirements_filepath = os.path.abspath(
    os.path.join(data_folder, "raw_extract_requirements.json")
)
with open(requirements_filepath, "r") as requirements_file:
    requirements = json.load(requirements_file)


outreach = pd.read_excel(
    os.path.abspath(os.path.join(data_folder, data_filename)),
    dtype=requirements["types"],
    parse_dates=requirements["date_columns"],
    usecols=requirements["types"].keys(),
)

# Change Column Names

outreach = outreach.rename(
    columns=requirements["rename"],
    errors="raise",
)

outreach["is_encampment"] = outreach["types"].str.contains("Encampment")

all_notes = (
    outreach["notes_1"].fillna("")
    + " |"
    + outreach["notes_2"].fillna("")
    + " |"
    + outreach["notes_outcome"].fillna("")
    + " |"
)

outreach["did_respond"] = all_notes != " | | |"

outreach["did_not_find_peh"] = all_notes.str.contains("no PEH", case=False)
outreach["declined_services"] = all_notes.str.contains("declined", case=False)
outreach["accepted_services"] = all_notes.str.contains("accept", case=False)

outreach.info()

outreach.to_csv(
    os.path.join(os.path.dirname(data_folder), "outreach_extract.csv"), index=False
)
