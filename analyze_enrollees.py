import os
import pandas as pd

data_file = "./data/enrollees_extract.csv"

raw_df = pd.DataFrame()

filepath = os.path.abspath(data_file)

df = pd.read_csv(
    filepath,
    parse_dates=["Enrollments Project Start Date", "Enrollments Exit Date Filter Date"],
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
# afro_latino.info()
# Should be 'Black, African American, or African'
print(pd.unique(afro_latino["Clients Race / Ethnicity"]))

# Should be 'Black, African American, or African'
print(pd.unique(afro_latino["Clients Race Cleaned"]))

# Should only have 4 groups Male, Female, Other, Unknown
print(pd.unique(df["Clients Gender Cleaned"]))

# Should only have 3 groups Yes, No, Unknown
print(pd.unique(df["Clients Veteran Status Cleaned"]))

# df[df["Programs Project Type Category"] == "Permanent Housing"]["Services Name"].value_counts().to_csv("./data/perm_counts.csv")

# df[df["Programs Project Type Category"] == "Interim Housing"]["Services Name"].value_counts().to_csv("./data/inter_counts.csv")

# df[df["Programs Project Type Category"] == "Services"]["Services Name"].value_counts().to_csv("./data/services_counts.csv")
