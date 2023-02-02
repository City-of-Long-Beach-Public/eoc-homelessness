import os
import pandas as pd

import utils

data_folder = "./data/enrollees_extract"

raw_df = pd.DataFrame()
for filename in os.listdir(data_folder):
    if filename != ".gitignore":
        filepath = os.path.abspath(os.path.join(data_folder, filename))

        parts_df = pd.read_csv(
            filepath,
            index_col=0,
            parse_dates=["Project Start Date", "Exit Date Filter Date"],
        )
        raw_df = pd.concat([raw_df, parts_df], ignore_index=True)

clean_df = raw_df

# Change Column Names

clean_df = clean_df.rename(
    columns={
        "Unique Identifier": "Clients Unique Identifier",
        "Project Start Date": "Enrollments Project Start Date",
        "Project Type Code": "Programs Project Type Code",
        "Full Name": "Programs Full Name",
        "Exit Date Filter Date": "Enrollments Exit Date Filter Date",
        "Destination": "Update/Exit Screen Destination",
        "Destination Category": "Update/Exit Screen Destination Category",
        "Days in Project": "Enrollments Days in Project",
        "Current Age": "Clients Current Age",
        "Ethnicity": "Clients Ethnicity",
        "Race": "Clients Race",
        "Veteran Status": "Clients Veteran Status",
        "Name": "Services Name",
        "Chronically Homeless at Project Start - Individual": "Entry Screen Chronically Homeless at Project Start - Individual",
        "Age at Project Start": "Entry Screen Age at Project Start",
        "Gender": "Clients Gender",
        "Full Geolocation": "Program Sites Full Geolocation",
        "Full Geolocation.1": "Service Geolocation",
    },
    errors="raise",
)

# Drop PII

clean_df = clean_df.drop(columns=["Date of Birth Date"], errors="ignore")

# Add Calculations


clean_df["Clients Race Cleaned"] = clean_df.apply(utils.clean_race, axis="columns")


clean_df["Clients Race / Ethnicity"] = clean_df.apply(
    utils.combine_race_ethnicity, axis="columns"
)


clean_df["Clients Gender Cleaned"] = clean_df.apply(utils.clean_gender, axis="columns")


clean_df["Clients Veteran Status Cleaned"] = clean_df.apply(
    utils.clean_veteran, axis="columns"
)

clean_df["is Program Event"] = clean_df.apply(utils.determine_program, axis="columns")


clean_df["Program Outcome"] = clean_df.apply(utils.determine_outcomes, axis="columns")

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
    utils.bin_type_code, axis="columns"
)


# raw_df.info()
clean_df.info()
clean_df.to_csv(
    os.path.join(os.path.dirname(data_folder), "enrollees_extract.csv"), index=False
)
