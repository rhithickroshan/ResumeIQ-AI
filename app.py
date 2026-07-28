import streamlit as st
import os

# Must be the very first Streamlit command
st.set_page_config(
    page_title="ResumeIQ AI | Premium ATS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    css_path = os.path.join("assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    inject_custom_css()
    
    # Hero Section
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>ResumeIQ AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--text-secondary); font-size: 1.2rem;'>Beat Every ATS with Machine Learning & Contextual AI.</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 99% Accuracy\nSemantic analysis beyond keyword matching.")
    with col2:
        st.success("### 50K+ Analyzed\nTrusted by job seekers globally.")
    with col3:
        st.warning("### 4.9★ Rating\nPremium insights via Gemini 1.5.")

    st.markdown("<br><br><center><h3>👈 Select 'Upload' from the sidebar to begin analysis.</h3></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()