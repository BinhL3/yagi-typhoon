import os
import pandas as pd

CSV_FOLDER = "csv/"

OUTPUT_FILE = "mttq.csv"

def merge_csv_files(csv_folder, output_file):
    dataframes = []
    
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_folder, filename)
            print(f"Processing file: {file_path}")
            df = pd.read_csv(file_path)
            dataframes.append(df)
    
    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")

if __name__ == "__main__":
    merge_csv_files(CSV_FOLDER, OUTPUT_FILE)
