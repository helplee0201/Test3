import streamlit as st
import pandas as pd
from utils.data import get_daily_details

# Set page configuration to wide
st.set_page_config(page_title="일별 상세 내역", layout="wide", initial_sidebar_state="collapsed")

# Apply custom CSS
st.markdown('<link href="styles.css" rel="stylesheet">', unsafe_allow_html=True)

# Initialize session state if needed
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'transaction_type' not in st.session_state:
    st.session_state.transaction_type = "매출"

def daily_details_page():
    # Check login status
    if not st.session_state.logged_in:
        st.error("로그인 후 이용해 주세요.")
        try:
            st.switch_page("login.py")
        except Exception as e:
            st.error(f"로그인 페이지로 전환 실패: {str(e)}")
        st.stop()
    
    # Check if selected_row is available
    if not st.session_state.selected_row:
        st.error("상세 내역을 조회할 데이터가 없습니다. 정보 조회 페이지로 돌아가세요.")
        try:
            st.switch_page("pages/2_info.py")
        except Exception as e:
            st.error(f"정보 조회 페이지로 전환 실패: {str(e)}")
        st.stop()
    
    # Header
    st.markdown('<div class="header"><h1>일별 상세 내역</h1></div>', unsafe_allow_html=True)
    
    # Main container
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        selected_row = st.session_state.selected_row
        transaction_type = st.session_state.transaction_type
        biz_num = selected_row.get("사업자등록번호", "")
        year_month = selected_row.get("기준년월", "")
        partner_biz_num = selected_row.get("매출처사업자번호" if transaction_type == "매출" else "매입처사업자번호", "")
        partner_name = selected_row.get("매출처명" if transaction_type == "매출" else "매입처명", "")
        
        st.markdown(f"<h2>{transaction_type} 상세 내역: {year_month} - {partner_name} ({partner_biz_num})</h2>", unsafe_allow_html=True)
        
        daily_data = get_daily_details(biz_num, year_month, partner_biz_num, transaction_type)
        
        if daily_data:
            DAILY_COLUMNS = [
                "전표발생일", "사업자등록번호",
                "매출처사업자번호" if transaction_type == "매출" else "매입처사업자번호",
                "매출처명" if transaction_type == "매출" else "매입처명",
                "계정과목", "구분","금액", "적요"
            ]
            
            df_daily = pd.DataFrame(daily_data)
            for col in DAILY_COLUMNS:
                if col not in df_daily.columns:
                    df_daily[col] = pd.NA
            df_daily = df_daily[DAILY_COLUMNS]
            
            st.dataframe(df_daily, use_container_width=True)
        else:
            st.warning("해당 조건으로 일별 상세 데이터가 없습니다.")
        
        if st.button("정보 조회 페이지로 돌아가기", use_container_width=True):
            st.session_state.selected_row = None
            try:
                st.switch_page("pages/2_info.py")
            except Exception as e:
                st.error(f"정보 조회 페이지로 전환 실패: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2025 테크핀레이팅스. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    daily_details_page()
