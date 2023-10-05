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

without_weird_hyphen = df["Programs Project Type Code"].str.replace('–', '-')

print(df["Programs Project Type Code"].unique())
print(without_weird_hyphen.unique())


# enroll_time_df = df[df["Programs Project Type Category"] == "Permanent Housing"][
#     df["Enrollments Project Start Date"] > pd.to_datetime("01/01/2021")
# ]

# enroll_2021_df = enroll_time_df[
#     enroll_time_df["Enrollments Project Start Date"] < pd.to_datetime("01/01/2022")
# ]
# enroll_2022_df = enroll_time_df[
#     enroll_time_df["Enrollments Project Start Date"] > pd.to_datetime("01/01/2022")
# ]

# enroll_2021_df.info()
# enroll_2022_df.info()

# same_day_enroll = enroll_time_df[pd.isna(enroll_time_df["Days since last Enrollment"])]
# print(same_day_enroll["Programs Project Type Code"].value_counts(normalize = True))
# print(enroll_time_df["Programs Project Type Code"].value_counts(normalize = True))


# grouped_enroll = df.groupby(["Clients Unique Identifier", "Enrollments Project Start Date", "Programs Full Name"]).size().apply(lambda x: x)
# grouped_enroll.info()

# grouped_enroll.to_csv("./data/enroll_same_day.csv")

# blank_service_names = df[df["Services Name"].isna()]

# print(blank_service_names)
# df[df["Programs Project Type Category"] == "Permanent Housing"]["Services Name"].value_counts().to_csv("./data/perm_counts.csv")

# df[df["Programs Project Type Category"] == "Interim Housing"]["Services Name"].value_counts().to_csv("./data/inter_counts.csv")

# df[df["Programs Project Type Category"] == "Services"]["Services Name"].value_counts().to_csv("./data/services_counts.csv")
