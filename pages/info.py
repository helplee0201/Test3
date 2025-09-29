import streamlit as st
import pandas as pd
from utils.data import get_filtered_data

# Set page configuration to wide
st.set_page_config(page_title="정보 조회", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'transaction_type' not in st.session_state:
    st.session_state.transaction_type = "매출"

# Define columns for Sales and Purchases
SALES_COLUMNS = [
    "기준년월", "사업자등록번호", "법인등록번호", "공급시기",
    "매출처사업자번호", "매출처명", "공급가액", "부가세",
    "매출유형", "공급건수", "취소건수", "취소금액",
    "총공급가액", "총취소금액", "거래비중"
]
PURCHASE_COLUMNS = [
    "기준년월", "사업자등록번호", "법인등록번호", "공급시기",
    "매입처사업자번호", "매입처명", "공급가액", "부가세",
    "매입유형", "공급건수", "취소건수", "취소금액",
    "총공급가액", "총취소금액", "거래비중"
]

def info_page():
    # Check login status
    if not st.session_state.logged_in:
        st.error("로그인 후 이용해 주세요.")
        try:
            st.switch_page("login.py")  # Redirect to login page
        except Exception as e:
            st.error(f"로그인 페이지로 전환 실패: {str(e)}")
        st.stop()  # Halt execution if not logged in
    else:
        st.title("정보 조회 페이지")
        
        # Header with input fields
        with st.container():
            st.subheader("조회 조건")
            col1, col2, col3 = st.columns([1, 1, 2])  # Three columns: biz_num, type, date range
            with col1:
                biz_num = "123-45-67890"
                st.text_input("사업자등록번호", value=biz_num, disabled=True)
            with col2:
                transaction_type = st.selectbox("매출/매입", ["매출", "매입"], key="transaction_type_select")
                st.session_state.transaction_type = transaction_type
            with col3:
                # Nested columns for start and end year-month pickers in one row
                start_col, end_col = st.columns(2)
                with start_col:
                    years = list(range(2020, 2030))
                    months = [f"{m:02d}" for m in range(1, 13)]
                    start_year = st.selectbox("시작년도", years, index=years.index(2025), key="start_year")
                    start_month = st.selectbox("시작월", months, index=months.index("08"), key="start_month")
                    start_year_month = f"{start_year}-{start_month}"
                with end_col:
                    end_year = st.selectbox("종료년도", years, index=years.index(2025), key="end_year")
                    end_month = st.selectbox("종료월", months, index=months.index("09"), key="end_month")
                    end_year_month = f"{end_year}-{end_month}"
        
        if st.button("조회"):
            if biz_num:
                # Get filtered data
                filtered_data = get_filtered_data(biz_num, start_year_month, end_year_month, transaction_type)
                st.session_state.filtered_data = filtered_data
                st.session_state.page_number = 1  # Reset to first page
                if filtered_data:
                    st.subheader("조회 결과")
                else:
                    st.warning("해당 조건으로 데이터가 없습니다.")
        
        # Display paginated data
        if st.session_state.filtered_data:
            df = pd.DataFrame(st.session_state.filtered_data)
            # Select columns based on transaction type
            columns = SALES_COLUMNS if st.session_state.transaction_type == "매출" else PURCHASE_COLUMNS
            # Rename DataFrame columns to match the display columns
            if st.session_state.transaction_type == "매출":
                df = df.rename(columns={
                    "매출처사업자번호": "매출처사업자번호",
                    "매출처명": "매출처명",
                    "매출유형": "매출유형"
                })
            else:
                df = df.rename(columns={
                    "매입처사업자번호": "매입처사업자번호",
                    "매입처명": "매입처명",
                    "매입유형": "매입유형"
                })
            df = df[columns]  # Reorder columns
            rows_per_page = 100
            total_rows = len(df)
            total_pages = (total_rows + rows_per_page - 1) // rows_per_page
            
            # Pagination controls
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("◄ 이전", disabled=(st.session_state.page_number <= 1)):
                    st.session_state.page_number = max(1, st.session_state.page_number - 1)
            with col2:
                st.write(f"페이지 {st.session_state.page_number} / {total_pages}")
            with col3:
                if st.button("다음 ►", disabled=(st.session_state.page_number >= total_pages)):
                    st.session_state.page_number = min(total_pages, st.session_state.page_number + 1)
            
            # Display current page data
            start_idx = (st.session_state.page_number - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)

if __name__ == "__main__":
    info_page()