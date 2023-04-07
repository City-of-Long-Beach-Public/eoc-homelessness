import os
import pandas as pd

import cleaners
import json


data_folder = "./data/enrollees_extract"

requirements_filepath = os.path.abspath(
    os.path.join(data_folder, "raw_extract_requirements.json")
)
with open(requirements_filepath, "r") as requirements_file:
    requirements = json.load(requirements_file)


raw_df = pd.DataFrame()
for filename in os.listdir(data_folder):
    if "HSB Program Enrollees" in filename:
        filepath = os.path.abspath(os.path.join(data_folder, filename))

        parts_df = pd.read_csv(
            filepath,
            index_col=0,
            dtype=requirements["types"],
            parse_dates=requirements["date_columns"],
        )
        raw_df = pd.concat([raw_df, parts_df], ignore_index=True)

clean_df = raw_df

# Change Column Names

clean_df = clean_df.rename(
    columns=requirements["rename"],
    errors="raise",
)

# Drop PII

clean_df = clean_df.drop(columns=["Date of Birth Date"], errors="ignore")

# Add Calculations


clean_df["Clients Race Cleaned"] = clean_df.apply(cleaners.clean_race, axis="columns")


clean_df["Clients Race / Ethnicity"] = clean_df.apply(
    cleaners.combine_race_ethnicity, axis="columns"
)


clean_df["Clients Gender Cleaned"] = clean_df.apply(
    cleaners.clean_gender, axis="columns"
)


clean_df["Clients Veteran Status Cleaned"] = clean_df.apply(
    cleaners.clean_veteran, axis="columns"
)

clean_df["is Service Event"] = clean_df.apply(
    cleaners.determine_service_event, axis="columns"
)

clean_df["Age Group at Project Start"] = pd.cut(
    clean_df["Entry Screen Age at Project Start"],
    [0, 17, 24, 34, 44, 54, 64, 74, 200],
    labels=["0-17", "18-24","25-34", "35-44", "45-54", "55-64", "65-74", "75+"],
)

clean_df[["Destination Cleaned", "Destination Category Cleaned"]] = clean_df.apply(
    cleaners.clean_destination, axis="columns", result_type="expand"
)

clean_df["Program Outcome"] = clean_df.apply(
    cleaners.determine_outcomes, axis="columns"
)

clean_df[
    [
        "Number of Previous Enrollments",
        "Number of Previous Enrollments (Last Year)",
        "Days since last Enrollment",
        "Days since first Enrollment",
        "Days since first Enrollment (Last Year)",
    ]
] = clean_df.apply(
    cleaners.add_prev_enrollments,
    axis="columns",
    result_type="expand",
    original_df=clean_df,
)

clean_df["Program Sites Lat"] = clean_df["Program Sites Full Geolocation"].replace(
    to_replace=",.+", value="", regex=True
)
clean_df["Program Sites Long"] = clean_df["Program Sites Full Geolocation"].replace(
    to_replace=".+,", value="", regex=True
)
clean_df["Service Lat"] = clean_df["Service Geolocation"].replace(
    to_replace=",.+", value="", regex=True
)
clean_df["Service Long"] = clean_df["Service Geolocation"].replace(
    to_replace=".+,", value="", regex=True
)


clean_df["Programs Project Type Category"] = clean_df.apply(
    cleaners.bin_type_code, axis="columns"
)


# raw_df.info()
clean_df.info()
clean_df.to_csv(
    os.path.join(os.path.dirname(data_folder), "enrollees_extract.csv"), index=False
)
