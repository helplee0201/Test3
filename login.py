import streamlit as st
import os
import sys

# Add parent directory to sys.path to ensure utils is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import check_credentials

# Set page configuration to centered
st.set_page_config(page_title="로그인", layout="centered")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # Display logo above input fields
    st.image("./logo.png", width=300)
    
    st.title("로그인 페이지")
    username = st.text_input("아이디", value="fixed_user", disabled=True, placeholder="아이디를 입력하세요")
    password = st.text_input("패스워드", value="fixed_password", type="password", disabled=True, placeholder="패스워드를 입력하세요")
    
    if st.button("조회"):
        st.session_state.logged_in = True
        try:
            st.switch_page("pages/info.py")
        except Exception as e:
            st.error(f"info.py로 전환 실패: {str(e)}")

if __name__ == "__main__":
    login_page()