import os
import pandas as pd

import utils
import json


data_folder = "./data/enrollees_extract"

raw_requirements_filepath =  os.path.abspath(os.path.join(data_folder, "raw_extract_requirements.json"))
with open(raw_requirements_filepath, "r") as raw_requirements_file:
    raw_requirements = json.load(raw_requirements_file)


raw_df = pd.DataFrame()
for filename in os.listdir(data_folder):
    if "HSB Program Enrollees" in filename:
        filepath = os.path.abspath(os.path.join(data_folder, filename))

        parts_df = pd.read_csv(
            filepath,
            index_col=0,
            dtype=raw_requirements["types"],
            parse_dates=raw_requirements["date_columns"],
        )
        raw_df = pd.concat([raw_df, parts_df], ignore_index=True)

clean_df = raw_df

# Change Column Names

clean_df = clean_df.rename(
    columns=raw_requirements["rename"],
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

clean_df["is Service Event"] = clean_df.apply(
    utils.determine_service_event, axis="columns"
)

clean_df["Age Group at Project Start"] = pd.cut(
    clean_df["Entry Screen Age at Project Start"],
    [0, 17, 24, 61, 200],
    labels=["0-17", "18-24", "25-61", "62+"],
)


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
