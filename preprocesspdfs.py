import pdfplumber
import re
import os
import pandas as pd

DATA_FOLDER = "data/"

# Function to handle 'file1_9-10_9.pdf' format
def extract_donations_format1(lines, page_number, file_name):
    donations = []
    # Regex pattern for 'file1_9-10_9.pdf' format
    # Pattern: Date DocNo Debit Credit Balance Content
    transaction_pattern = re.compile(
        r'^(?P<date>\d{2}/\d{2}/\d{4})\s+'
        r'(?P<doc_no>\d+)\s+'
        r'(?P<debit>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<credit>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<balance>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<content>.+)$'
    )

    for line in lines:
        match = transaction_pattern.match(line)
        if match:
            transaction_code = match.group('doc_no')
            amount = match.group('credit') if match.group('credit') and match.group('credit') != '-' else match.group('debit')
            amount = amount.replace(',', '') if amount and amount != '-' else '0'
            transaction_detail = match.group('content')
            donations.append({
                "transaction_code": transaction_code,
                "amount": amount,
                "transaction_detail": transaction_detail.strip(),
                "page": page_number + 1,
                "file": file_name
            })
    return donations

# Function to handle '9_9-12_9.pdf' format
def extract_donations_format2(lines, page_number, file_name):
    donations = []
    # Regex pattern for '9_9-12_9.pdf' format
    # Pattern: Date Remark Dr Cr Balance RefNo
    transaction_pattern = re.compile(
        r'^(?P<date>\d{2}/\d{2}/\d{4})\s+'
        r'(?P<remark>.+?)\s+'
        r'(?P<debit>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<credit>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<balance>\d{1,3}(?:,\d{3})*|\-)?\s+'
        r'(?P<ref_no>\d+)$'
    )

    for line in lines:
        match = transaction_pattern.match(line)
        if match:
            transaction_code = match.group('ref_no')
            amount = match.group('credit') if match.group('credit') and match.group('credit') != '-' else match.group('debit')
            amount = amount.replace(',', '') if amount and amount != '-' else '0'
            transaction_detail = match.group('remark')
            donations.append({
                "transaction_code": transaction_code,
                "amount": amount,
                "transaction_detail": transaction_detail.strip(),
                "page": page_number + 1,
                "file": file_name
            })
    return donations

# Main function to handle different PDF formats
def extract_donations_from_pdf(file_path):
    donations = []
    file_name = os.path.basename(file_path)
    
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                # Determine which format to use based on the file name
                if "1_9-10_9" in file_name:
                    donations.extend(extract_donations_format1(lines, page_number, file_name))
                elif "9_9-12_9" in file_name:
                    donations.extend(extract_donations_format2(lines, page_number, file_name))
                else:
                    # Handle unknown formats if necessary
                    print(f"Unknown format for file {file_name}. Skipping.")
    return donations

# Processing all PDFs
all_donations = []

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".pdf"):
        file_path = os.path.join(DATA_FOLDER, filename)
        print(f"Processing: {filename}")
        donations = extract_donations_from_pdf(file_path)
        all_donations.extend(donations)

# Convert the list of donations to a Pandas DataFrame
df = pd.DataFrame(all_donations, columns=["transaction_code", "amount", "transaction_detail", "page", "file"])

# Convert amount to numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

# Save the processed data to a CSV file
df.to_csv("preprocessed_donations.csv", index=False)

print("PDFs processed and saved to preprocessed_donations.csv")
