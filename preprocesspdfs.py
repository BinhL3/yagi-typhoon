import pdfplumber
import re
import os
import pandas as pd

# Folder where all PDF files are stored
DATA_FOLDER = "data/"

# Function to process a single PDF and extract donations
def extract_donations_from_pdf(file_path):
    donations = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:  # Only process if the page has text
                lines = text.split("\n")
                donation_pattern = re.compile(r'(?P<name>[\w\s]+)\s+(?P<donation_amount>\d{1,3}(,\d{3})*)')

                for line in lines:
                    match = donation_pattern.search(line)
                    if match:
                        name = match.group('name')
                        donation_amount = match.group('donation_amount')
                        donations.append({
                            "name": name, 
                            "donation_amount": donation_amount, 
                            "page": page_number + 1,
                            "file": os.path.basename(file_path)
                        })
    return donations

# Pre-process all PDFs in the folder and save to CSV
all_donations = []

# Loop through all PDF files in the 'data/' folder
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".pdf"):
        file_path = os.path.join(DATA_FOLDER, filename)
        print(f"Processing: {filename}")
        donations = extract_donations_from_pdf(file_path)
        all_donations.extend(donations)

# Convert the list of donations to a Pandas DataFrame
df = pd.DataFrame(all_donations)

# Save the processed data to a CSV file
df.to_csv("preprocessed_donations.csv", index=False)

print("PDFs processed and saved to preprocessed_donations.csv")
