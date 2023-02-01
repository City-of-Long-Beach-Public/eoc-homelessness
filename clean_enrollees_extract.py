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


def clean_race(row):
    out = row["Clients Race"]
    if row["Black, African American, or African"] == "Yes":
        out = "Black, African American, or African"
    if out in {"Client doesn't know", "Client refused", "Data not collected"}:
        out = "Unknown"
    return out


clean_df["Clients Race Cleaned"] = clean_df.apply(clean_race, axis="columns")


def combine_race_ethnicity(row):
    out = row["Clients Race Cleaned"]

    if (row["Clients Ethnicity"] == "Hispanic/Latin(a)(o)(x)") & (
        out != "Black, African American, or African"
    ):
        out = "Hispanic/Latin(a)(o)(x)"
    return out


clean_df["Clients Race / Ethnicity"] = clean_df.apply(
    combine_race_ethnicity, axis="columns"
)


def clean_gender(row):
    other_set = {
        "Questioning",
        "Transgender",
        "A gender other than singularly female or male (e.g., non-binary, genderfluid, agender, culturally specific gender)",
    }
    unknown_set = {"Client doesn't know", "Client refused", "Data not collected"}
    out = row["Clients Gender"]
    if out in other_set:
        out = "Other"
    if out in unknown_set:
        out = "Unknown"
    return out


clean_df["Clients Gender Cleaned"] = clean_df.apply(clean_gender, axis="columns")


def clean_veteran(row):
    unknown_set = {"Client doesn't know", "Client refused", "Data not collected"}
    out = row["Clients Veteran Status"]
    if (out in unknown_set) | (pd.isna(out)):
        out = "Unknown"
    return out


clean_df["Clients Veteran Status Cleaned"] = clean_df.apply(
    clean_veteran, axis="columns"
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


def bin_type_code(code):
    interim_set = {"Emergency Shelter", "Transitional Housing", "Safe Haven"}
    permanent_set = {
        "PH - Rapid Re-Housing",
        "PH - Housing Only",
        "PH - Housing with Services (no disability required for entry)",
        "PH - Permanent Supportive Housing (disability required for entry)",
    }
    services_set = {
        "Street Outreach",
        "Coordinated Entry",
        "Homelessness Prevention",
        "Services Only",
        "Other",
    }

    if code in interim_set:
        return "Interim Housing"
    if code in permanent_set:
        return "Permanent Housing"
    if code in services_set:
        return "Services"


clean_df["Programs Project Type Category"] = clean_df[
    "Programs Project Type Code"
].transform(bin_type_code)


# raw_df.info()
clean_df.info()
clean_df.to_csv(
    os.path.join(os.path.dirname(data_folder), "enrollees_extract.csv"), index=False
)
