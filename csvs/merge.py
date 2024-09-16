import pandas as pd
import glob

csv_files = glob.glob("*.csv")

df_list = []

for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv("mttq.csv", index=False)