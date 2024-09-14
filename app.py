import streamlit as st
import pandas as pd

st.title("Donation Amount Query Dashboard")

try:
    df = pd.read_csv("preprocessed_donations.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Preprocessed data not found. Please run the pre-processing script first.")
    df = None

if df is not None:
    search_query = st.text_input("Enter the name to search for donations:")
    
    if search_query:
        filtered_df = df[df['name'].str.contains(search_query, case=False, na=False)]
        
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} donation(s) matching '{search_query}':")
            st.dataframe(filtered_df)
        else:
            st.write(f"No donations found for '{search_query}'.")