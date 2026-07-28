import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Analysis Dashboard | ResumeIQ", layout="wide")

if 'analysis_results' not in st.session_state:
    st.warning("Please upload a resume first.")
    st.stop()

results = st.session_state['analysis_results']
score = results['overall_score']

st.title("📊 ATS Analysis Report")

# Top KPI Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Overall ATS Score", f"{score}%", delta="High Probability" if score > 75 else "- Needs Work")
c2.metric("Semantic Match", f"{results['semantic_score']}%")
c3.metric("Hard Skills Match", f"{results['skill_match_score']}%")

st.write("---")

# Visualizations
col_chart, col_skills = st.columns([1, 1])

with col_chart:
    st.subheader("Match Breakdown")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ATS Fit"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#3B82F6"},
            'steps': [
                {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.3)"},
                {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.3)"},
                {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.3)"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

with col_skills:
    st.subheader("Skill Gap Analysis")
    st.success(f"**Matched Skills:** {', '.join(results['matched_skills']).title() if results['matched_skills'] else 'None'}")
    st.error(f"**Missing Skills:** {', '.join(results['missing_skills']).title() if results['missing_skills'] else 'None'}")
    
    st.progress(results['skill_match_score'] / 100.0, text="Skill Coverage")