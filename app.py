import streamlit as st
import pandas as pd

st.title("MTTQ Donations Dashboard")

def format_vnd(amount):
    return f"{float(amount):,}".replace(",", ".") + " VNĐ"

try:
    df = pd.read_csv("mttq.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("CSV file not found. Please make sure 'mttq.csv' exists in the directory.")
    df = None

if df is not None:
    search_query = st.text_input("Enter search query for transaction code, amount, or transaction detail:")
    
    if search_query:
        filtered_df = df[
            df['transaction_code'].astype(str).str.contains(search_query, case=False, na=False) |
            df['amount'].astype(str).str.contains(search_query, case=False, na=False) |
            df['transaction_detail'].str.contains(search_query, case=False, na=False)
        ]
        
        if not filtered_df.empty:
            filtered_df['amount'] = filtered_df['amount'].apply(format_vnd)
            st.write(f"Found {len(filtered_df)} donation(s) matching your criteria:")
            st.dataframe(filtered_df)
        else:
            st.write("No donations found matching your search criteria.")
