import streamlit as st
import pandas as pd
import json
import os
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Settings | ResumeIQ AI", layout="wide")

# Inject Custom CSS
css_path = os.path.join("assets", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

db = DatabaseManager()

st.title("⚙️ System Settings & Data Management")
st.write("Manage API credentials, view persistent history, export audit logs, or reset application state.")

st.write("---")

tab_api, tab_history, tab_system = st.tabs(["🔑 API & AI Models", "📜 History & Export", "🛠 System Maintenance"])

# Tab 1: API Config
with tab_api:
    st.subheader("Google Gemini API Configuration")
    current_key = st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))
    
    api_key_input = st.text_input(
        "Gemini API Key", 
        value=current_key, 
        type="password",
        help="Provide your API key to enable AI rewrite suggestions and interview generation."
    )
    
    col_save, col_clear = st.columns([1, 4])
    with col_save:
        if st.button("Save API Key", use_container_width=True):
            st.session_state["gemini_api_key"] = api_key_input
            st.success("API Key updated successfully!")
            
    st.info("💡 **Security Note:** API Keys stored here remain strictly in memory for your current session.")

# Tab 2: History & Data Export
with tab_history:
    st.subheader("Analysis Audit Trail")
    history_records = db.get_all_history()
    
    if not history_records:
        st.write("No audit records found in database.")
    else:
        df_history = pd.DataFrame(history_records)
        
        search_query = st.text_input("🔍 Search by Filename or Role", "")
        if search_query:
            df_history = df_history[
                df_history['filename'].str.contains(search_query, case=False, na=False) |
                df_history['job_role'].str.contains(search_query, case=False, na=False)
            ]
        
        st.dataframe(
            df_history[['id', 'filename', 'job_role', 'overall_score', 'created_at']],
            use_container_width=True,
            hide_index=True
        )
        
        st.subheader("Export Data")
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv_data = df_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export History as CSV",
                data=csv_data,
                file_name="resumeiq_analysis_history.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with col_exp2:
            json_data = json.dumps(history_records, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Export History as JSON",
                data=json_data,
                file_name="resumeiq_analysis_history.json",
                mime="application/json",
                use_container_width=True
            )

# Tab 3: System Maintenance
with tab_system:
    st.subheader("Danger Zone")
    st.warning("Clearing history will permanently remove all stored scan metrics from your local SQLite database.")
    
    if st.button("🚨 Clear All Analysis History", type="secondary"):
        db.clear_all_history()
        st.success("Database cleared successfully!")
        st.rerun()