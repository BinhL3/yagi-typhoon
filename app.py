import streamlit as st
import pandas as pd

st.title("Donation Amount Query Dashboard")

# Load the CSV file (mttq.csv) with transaction_code, amount, and transaction_detail
try:
    df = pd.read_csv("mttq.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("CSV file not found. Please make sure 'mttq.csv' exists in the directory.")
    df = None

if df is not None:
    # Input for searching transaction detail
    search_query = st.text_input("Enter the content/transaction detail to search for donations:")

    # Input for searching by amount (optional, allows search by amount as well)
    amount_query = st.number_input("Enter donation amount to search for (optional):", min_value=0.0, value=0.0, step=1.0)

    # If a search query or amount is entered
    if search_query or amount_query > 0:
        # Filter by transaction detail content if search_query is provided
        if search_query:
            filtered_df = df[df['transaction_detail'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_df = df
        
        # Further filter by amount if amount_query is greater than 0
        if amount_query > 0:
            filtered_df = filtered_df[filtered_df['amount'] == amount_query]

        # Display the filtered results
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} donation(s) matching your criteria:")
            st.dataframe(filtered_df)
        else:
            st.write("No donations found matching your search criteria.")
