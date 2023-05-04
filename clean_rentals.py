import os
import pandas as pd

import json


data_folder = os.path.join(os.path.dirname(__file__), "data", "rentals_extract")

data_filename = "rental_case_summary.xlsx"


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
        "White": "White",
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


def determine_completeness(row):
    out = row["landlord_and_applicant_complete"]
    if (not pd.isna(row["source_grant_recipient"])) & (not pd.isna(row["source"])):
        if (row["source"] != "Landlord") & (
            row["source_grant_recipient"] == "Applicant"
        ):
            out = row["applicant_complete"]

    if out == "Yes":
        out = True
    else:
        out = False

    return out


# Change Column Names

rentals = rentals.rename(
    columns=requirements["rename"],
    errors="raise",
)

rentals = rentals.query('denial_reason != ["Testing/Training", "Duplicate"]')

zip_codes, uniques = pd.factorize(rentals["zip"])
id_codes, uniques = pd.factorize(rentals["id"])
combined_codes = pd.Series(zip_codes).where(zip_codes != -1, ((id_codes + 1) * -1))

rentals["client_id"] = combined_codes.array

rentals = rentals.drop(columns=["zip"])

rentals["is_complete"] = rentals.apply(determine_completeness, axis="columns")

rentals = rentals.drop(columns=["landlord_and_applicant_complete"])
rentals = rentals.drop(columns=["applicant_complete"])


rentals["cleaned_race"] = rentals.apply(HMISify_race, axis="columns")

rentals["race_ethnicity"] = rentals.apply(combine_race_ethnicity, axis="columns")

rentals["cleaned_gender"] = rentals.apply(clean_gender, axis="columns")

rentals["days_till_status_change"] = (
    rentals["date_status"] - rentals["date_submitted"]
).dt.days


rentals["age_group"] = pd.cut(
    rentals["age"],
    [0, 17, 24, 34, 44, 54, 64, 74, 200],
    labels=["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"],
)

rentals.info()

rentals.to_csv(
    os.path.join(os.path.dirname(data_folder), "rentals_extract.csv"), index=False
)
