import streamlit as st
from utils.parser import DocumentParser
from utils.ml_engine import MLResumeEngine

st.set_page_config(page_title="Upload Resume | ResumeIQ", layout="wide")

# Dummy skill DB for demonstration
TECH_SKILLS = ["python", "java", "machine learning", "nlp", "react", "aws", "docker", "kubernetes", "sql", "git"]

st.title("📄 Upload & Analyze")
st.write("Upload your resume and the target job description.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    resume_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx", "txt"])

with col2:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=150)

if st.button("🚀 Analyze with ML", use_container_width=True):
    if resume_file and jd_text:
        with st.spinner("Initializing ML Pipeline (NLP, TF-IDF, Transformers)..."):
            parser = DocumentParser()
            resume_text = parser.extract_text(resume_file)
            
            engine = MLResumeEngine()
            results = engine.generate_ats_score(resume_text, jd_text, TECH_SKILLS)
            
            # Save to session state for the analysis page
            st.session_state['analysis_results'] = results
            st.session_state['resume_text'] = resume_text
            st.session_state['jd_text'] = jd_text
            
            st.success("Analysis Complete! Navigate to the 'Analysis' tab in the sidebar.")
    else:
        st.error("Please provide both a resume and a job description.")