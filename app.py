import streamlit as st
import pandas as pd

st.markdown("""
    - Mình là [Binh](https://binhl3.github.io/) :smiley:
    - Liên hệ: [LinkedIn](https://www.linkedin.com/in/binhlee/) / bql23@drexel.edu
    - [YouTube](https://www.youtube.com/@binh) :shushing_face:
""")

st.title("Bảng thống kê quyên góp MTTQ")

def format_vnd(amount):
    return f"{float(amount):,}".replace(",", ".") + " VNĐ"

try:
    df = pd.read_csv("mttq.csv")
    st.success("Dữ liệu đã được tải thành công!")
except FileNotFoundError:
    st.error("Không tìm thấy tệp CSV. Vui lòng đảm bảo 'mttq.csv' tồn tại trong thư mục.")
    df = None

if df is not None:
    search_query = st.text_input("Nhập mã, số tiền hoặc nội dung giao dịch để tìm kiếm:")

    if search_query:
        filtered_df = df[
            df['transaction_code'].astype(str).str.contains(search_query, case=False, na=False) |
            df['amount'].astype(str).str.contains(search_query, case=False, na=False) |
            df['transaction_detail'].str.contains(search_query, case=False, na=False)
        ]
        
        if not filtered_df.empty:
            filtered_df['amount'] = filtered_df['amount'].apply(format_vnd)
            st.write(f"Tìm thấy {len(filtered_df)} giao dịch:")
            st.dataframe(filtered_df)
        else:
            st.write("Không tìm thấy giao dịch nào.")
