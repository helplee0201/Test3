import streamlit as st
import os
import sys

# Add parent directory to sys.path to ensure utils is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import check_credentials

# Set page configuration to centered
st.set_page_config(page_title="로그인", layout="centered")

# Apply custom CSS
st.markdown('<link href="styles.css" rel="stylesheet">', unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # Header
    st.markdown('<div class="header"><h1>사기거래 적발 시스템</h1></div>', unsafe_allow_html=True)
    
    # Main container
    with st.container():
        st.markdown('<div class="container">', unsafe_allow_html=True)
        # Display logo
        st.image("./logo.png", width=200)
        
        st.markdown("<h2>로그인</h2>", unsafe_allow_html=True)
        with st.form(key="login_form"):
            username = st.text_input("아이디", value="fixed_user", disabled=True, help="아이디는 fixed_user로 고정되어 있습니다.")
            password = st.text_input("패스워드", value="fixed_password", type="password", disabled=True, help="패스워드는 fixed_password로 고정되어 있습니다.")
            
            submit_button = st.form_submit_button("로그인", use_container_width=True)
            
            if submit_button:
                st.session_state.logged_in = True
                try:
                    st.switch_page("pages/2_info.py")
                except Exception as e:
                    st.error(f"정보 조회 페이지로 전환 실패: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2025 테크핀레이팅스. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    login_page()
