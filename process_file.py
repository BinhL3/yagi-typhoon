import pdfplumber
import re
import os
import pandas as pd

DATA_FOLDER = "data/"
CSV_OUTPUT_FOLDER = "csv/" 
OUTPUT_FILE = "mttq.csv" 

def extract_donations_agribank(lines, page_number, file_name):
    donations = []
    
    # Modified pattern to ensure Credit (CR) is used as the transaction amount
    transaction_pattern = re.compile(
        r'^(?P<date>\d{2}/\d{2}/\d{4})\s+'
        r'(?P<remark>.+?)\s+'
        r'(?P<debit>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?'  # Debit is optional
        r'(?P<credit>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?'  # Credit is optional (this is the transaction amount)
        r'(?P<balance>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?' # Balance is optional
        r'(?P<ref_no>\d+)$'
    )

    unmatched_lines = []  # For tracking lines that don't match the pattern

    for line in lines:
        match = transaction_pattern.match(line)
        if match:
            transaction_code = match.group('ref_no')
            amount = match.group('credit').replace(',', '') if match.group('credit') and match.group('credit') != '-' else '0'  # Using Credit (CR) as the amount
            transaction_detail = match.group('remark')
            donations.append({
                "transaction_code": transaction_code,
                "amount": amount,
                "transaction_detail": transaction_detail.strip(),
                "page": page_number + 1,
                "file": file_name
            })
        else:
            unmatched_lines.append(line)  # Log the unmatched lines for further debugging

    return donations

def extract_donations_vietcombank(lines, page_number, file_name):
    donations = []
    transaction_pattern = re.compile(
        r'^(?P<date>\d{2}/\d{2}/\d{4})\s+'
        r'(?P<debit>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?'
        r'(?P<credit>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?' 
        r'(?P<balance>(?:\d{1,3}(?:,\d{3})*|\-)?\s+)?'
        r'(?P<transaction_content>.+)$'
    )

    unmatched_lines = []

    for line in lines:
        match = transaction_pattern.match(line)
        if match:
            date = match.group('date')
            debit = match.group('debit').replace(',', '') if match.group('debit') and match.group('debit') != '-' else '0'
            credit = match.group('credit').replace(',', '') if match.group('credit') and match.group('credit') != '-' else '0'
            balance = match.group('balance').replace(',', '') if match.group('balance') and match.group('balance') != '-' else '0'
            transaction_content = match.group('transaction_content').strip()
            donations.append({
                "date": date,
                "debit": debit,
                "credit": credit,
                "balance": balance,
                "transaction_content": transaction_content,
                "page": page_number + 1,
                "file": file_name
            })
        else:
            unmatched_lines.append(line) 

    return donations

def process_large_pdf(bank_name, city_name, file_number):
    file_name = f"{bank_name}_{city_name}_{file_number}.pdf"
    file_path = os.path.join(DATA_FOLDER, city_name, file_name)
    
    if not os.path.exists(file_path):
        print(f"File {file_name} not found in {os.path.join(DATA_FOLDER, city_name)}")
        return

    print(f"Processing: {file_path}")
    
    output_csv = os.path.join(CSV_OUTPUT_FOLDER, f"{bank_name}_{city_name}_{file_number}_donations.csv")
    
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                if bank_name.lower() == "vietcombank":  # Process Vietcombank files
                    donations = extract_donations_vietcombank(lines, page_number, file_name)

                    # Save results incrementally after each page
                    if donations:
                        df = pd.DataFrame(donations, columns=["date", "debit", "credit", "balance", "transaction_content", "page", "file"])
                        df.to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)
                elif bank_name.lower() == "agribank":  # Process Agribank files
                    donations = extract_donations_agribank(lines, page_number, file_name)

                    if donations:
                        df = pd.DataFrame(donations, columns=["transaction_code", "amount", "transaction_detail", "page", "file"])
                        df.to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)

    print(f"Finished processing {file_name} and saved results to {output_csv}")

def merge_csv_files(output_file):
    dataframes = []
    
    for filename in os.listdir(CSV_OUTPUT_FOLDER):
        if filename.endswith(".csv"):
            file_path = os.path.join(CSV_OUTPUT_FOLDER, filename)
            print(f"Merging file: {file_path}")
            df = pd.read_csv(file_path)
            dataframes.append(df)
    
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")

def main():
    bank_name = input("Enter the bank name (e.g., 'vietcombank'): ").strip().lower()
    city_name = input("Enter the city name (e.g., 'hanoi'): ").strip().lower()
    file_number = input("Enter the file number (e.g., '2'): ").strip()

    process_large_pdf(bank_name, city_name, file_number)

    merge_csv_files(OUTPUT_FILE)

if __name__ == "__main__":
    main()
