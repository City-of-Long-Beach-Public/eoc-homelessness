import os
import pandas as pd

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


raw_df.info()
clean_df.info()
raw_df.to_csv(
    os.path.join(os.path.dirname(data_folder), "enrollees_extract.csv"), index=False
)
