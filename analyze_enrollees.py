import os
import pandas as pd
import json

data_file = "./data/enrollees_extract.csv"

requirements_filepath = os.path.abspath("./data/enrollees_extract_requirements.json")
with open(requirements_filepath, "r") as requirements_file:
    requirements = json.load(requirements_file)

filepath = os.path.abspath(data_file)

df = pd.read_csv(
    filepath,
    dtype=requirements["types"],
    parse_dates=requirements["date_columns"],
    engine="python",
)

# df.info()

no_code_df = df[~df["Programs Project Type Category"].notna()]

unique_codes = pd.unique(no_code_df["Programs Project Type Code"])

print(unique_codes)

safe_haven = df[df["Programs Project Type Category"] == "Safe Haven"]

# Should be empty
print(pd.unique(safe_haven["Programs Full Name"]))
# Should be Empty
print(pd.unique(safe_haven["Services Name"]))


afro_latino = df.query(
    "`Clients Ethnicity` == 'Hispanic/Latin(a)(o)(x)' & `Clients Race` == 'Black, African American, or African'"
)

white_latino = df.query(
    "`Clients Ethnicity` == 'Hispanic/Latin(a)(o)(x)' & `Clients Race` == 'White'"
)

# afro_latino.info()
# Should be 'Black, African American, or African'
print(pd.unique(afro_latino["Clients Race / Ethnicity"]))

# Should be 'Black, African American, or African'
print(pd.unique(afro_latino["Clients Race Cleaned"]))

# Should be 'Hispanic/Latin(a)(o)(x)'
print(pd.unique(white_latino["Clients Race / Ethnicity"]))

# Should be 'White'
print(pd.unique(white_latino["Clients Race Cleaned"]))

# Should only have 4 groups Male, Female, Other, Unknown
print(pd.unique(df["Clients Gender Cleaned"]))

# Should only have 3 groups Yes, No, Unknown
print(pd.unique(df["Clients Veteran Status Cleaned"]))

# Should only have 5 groups Positive, Negative, Permanent, Temporary, Exclude
print(pd.unique(df["Program Outcome"]))

# Should just be logical list
print(pd.unique(df["is Service Event"]))

# Should only be interim, permanent, and Support Services
print(pd.unique(df["Programs Project Type Category"]))


# blank_service_names = df[df["Services Name"].isna()]

# print(blank_service_names)
# df[df["Programs Project Type Category"] == "Permanent Housing"]["Services Name"].value_counts().to_csv("./data/perm_counts.csv")

# df[df["Programs Project Type Category"] == "Interim Housing"]["Services Name"].value_counts().to_csv("./data/inter_counts.csv")

# df[df["Programs Project Type Category"] == "Services"]["Services Name"].value_counts().to_csv("./data/services_counts.csv")
