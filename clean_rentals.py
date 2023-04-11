import os
import pandas as pd

import json


data_folder = os.path.join(os.path.dirname(__file__), "data", "rentals_extract")

data_filename = "4_3_2023_casesummary.xlsx"


requirements_filepath = os.path.abspath(
    os.path.join(data_folder, "raw_extract_requirements.json")
)
with open(requirements_filepath, "r") as requirements_file:
    requirements = json.load(requirements_file)

rentals = pd.read_excel(
    os.path.abspath(os.path.join(data_folder, data_filename)),
    dtype=requirements["types"],
    parse_dates=requirements["date_columns"],
    usecols=requirements["types"].keys(),
)

def HMISify_race(row):
    race_dict = {
        "Black or African American": "Black, African American, or African",
        "American Indian or Alaska Native": "American Indian, Alaska Native, or Indigenous",
        "Multiple": "Multi-Racial",
        "Native Hawaiian or Pacific Islander": "Native Hawaiian or Pacific Islander",
        "Asian": "Asian or Asian American",
        "Other": "Unknown",
        "Decline to Answer": "Unknown",
        "White": "White"
    }
    return race_dict.get(row["race"], "Unknown")


def clean_gender(row):
    out = row["gender"]
    if pd.isna(out) | ((out != "Female") & (out != "Male")):
        out = "Gender Expansive or Declined"
    return out

def combine_race_ethnicity(row):
    out = row["cleaned_race"]

    if pd.isna(row["ethnicity"]):
        return out

    if (row["ethnicity"] == "Hispanic or Latino") & (
        out != "Black, African American, or African"
    ):
        out = "Hispanic/Latin(a)(o)(x)"
    return out


# Change Column Names

rentals = rentals.rename(
    columns=requirements["rename"],
    errors="raise",
)

rentals["cleaned_race"] = rentals.apply(
    HMISify_race, axis="columns"
)

rentals["race_ethnicity"] = rentals.apply(
    combine_race_ethnicity, axis="columns"
)

rentals["cleaned_gender"] = rentals.apply(
    clean_gender, axis="columns"
)
rentals["grant_net_total"] = rentals["grant_total"] - rentals["grant_refunded"]



rentals.info()

rentals.to_csv(
    os.path.join(os.path.dirname(data_folder), "rentals_extract.csv"), index=False
)
