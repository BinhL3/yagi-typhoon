import streamlit as st
import pandas as pd
import os
from datetime import datetime

language = st.radio("Chọn ngôn ngữ / Select Language:", ("Tiếng Việt", "English"))

try:
    last_modified_time = os.path.getmtime("mttq.csv")
    last_updated = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')
except FileNotFoundError:
    last_updated = None

if language == "English":
    st.markdown("""
        This project tracks donations to [MTTQ Việt Nam](https://www.facebook.com/mttqvietnam) by [Binh Le](https://binhl3.github.io/)
        
        [GitHub repo](https://github.com/BinhL3/yagi-typhoon/)

        Special thanks to [T-rektt](https://github.com/t-rekttt/mttq/tree/main/parsed) for the original parsers! <3
    """)
    st.title("MTTQ Donations Dashboard")
    search_input_label = "Enter transaction code, amount, or transaction detail to search:"
    data_loaded_message = "Data is ready!"
    file_not_found_message = "CSV file not found. Please ensure 'mttq.csv' exists in the directory."
    no_results_message = "No transactions found."
    results_message = "Found {} transactions:"
    last_updated_text = "Last Updated: "
else:
    st.markdown("""
        Dự án thống kê những số tiền ủng hộ [MTTQ Việt Nam](https://www.facebook.com/mttqvietnam) bởi [Binh Le](https://binhl3.github.io/)
        
        [GitHub repo](https://github.com/BinhL3/yagi-typhoon/)

        Cảm ơn anh [T-rektt](https://github.com/t-rekttt/mttq/tree/main/parsed) vì những cái parser gốc ạ <3
    """)
    st.title("Bảng thống kê quyên góp MTTQ")
    search_input_label = "Nhập mã, số tiền hoặc nội dung giao dịch để tìm kiếm:"
    data_loaded_message = "Dữ liệu đã sẵn sàng!"
    file_not_found_message = "Không tìm thấy tệp CSV. Vui lòng đảm bảo 'mttq.csv' tồn tại trong thư mục."
    no_results_message = "Không tìm thấy giao dịch nào."
    results_message = "Tìm thấy {} giao dịch:"
    last_updated_text = "Cập nhật lần cuối: "

if last_updated:
    st.markdown(f"**{last_updated_text} {last_updated}**")

def format_vnd(amount):
    try:
        amount = float(str(amount).replace(".", "").replace(",", ""))
        return f"{int(amount):,}".replace(",", ".") + " VNĐ"
    except ValueError:
        return amount

try:
    df = pd.read_csv("mttq.csv")
    st.success(data_loaded_message)
except FileNotFoundError:
    st.error(file_not_found_message)
    df = None

if df is not None:
    search_query = st.text_input(search_input_label)

    if search_query:
        filtered_df = df[
            df['transaction_code'].astype(str).str.contains(search_query, case=False, na=False) |
            df['amount'].astype(str).str.contains(search_query, case=False, na=False) |
            df['transaction_detail'].str.contains(search_query, case=False, na=False)
        ]
        
        if not filtered_df.empty:
            filtered_df['amount'] = filtered_df['amount'].apply(format_vnd)
            st.write(results_message.format(len(filtered_df)))
            st.dataframe(filtered_df)
        else:
            st.write(no_results_message)
