import os
import pandas as pd

data_folder = "./data/enrollees_extract"

raw_df = pd.DataFrame()
for filename in os.listdir(data_folder):
    if filename != ".gitignore":
        filepath = os.path.abspath(os.path.join(data_folder, filename))

        parts_df = pd.read_csv(filepath)
        raw_df = pd.concat([raw_df, parts_df], ignore_index=True)

raw_df.info()
raw_df.to_csv(
    os.path.join(os.path.dirname(data_folder), "enrollees_extract.csv"), index=False
)
