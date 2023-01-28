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

print(pd.unique(safe_haven["Programs Full Name"]))

print(pd.unique(safe_haven["Services Name"]))


afro_latino = df.query(
    "`Clients Ethnicity` == 'Hispanic/Latin(a)(o)(x)' & `Clients Race` == 'Black, African American, or African'"
)
afro_latino.info()
print(pd.unique(afro_latino["Clients Race / Ethnicity"]))
