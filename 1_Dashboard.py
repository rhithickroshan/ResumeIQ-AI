import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Dashboard | ResumeIQ AI", layout="wide")

# Inject Custom CSS
css_path = os.path.join("assets", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

db = DatabaseManager()
stats = db.get_summary_stats()
history_records = db.get_all_history()

st.title("⚡ Executive Analytics Dashboard")
st.markdown("Overview of your resume optimizations, ATS score distributions, and performance metrics.")

st.write("---")

# KPI Summary Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div style="background: rgba(18, 20, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px;">
        <p style="color: #9CA3AF; margin: 0; font-size: 0.9rem;">Total Resumes Analyzed</p>
        <h2 style="margin: 5px 0 0 0; font-size: 2.2rem; color: #3B82F6;">{stats['total_analyzed']}</h2>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div style="background: rgba(18, 20, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px;">
        <p style="color: #9CA3AF; margin: 0; font-size: 0.9rem;">Average ATS Score</p>
        <h2 style="margin: 5px 0 0 0; font-size: 2.2rem; color: #10B981;">{stats['avg_score']}%</h2>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div style="background: rgba(18, 20, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px;">
        <p style="color: #9CA3AF; margin: 0; font-size: 0.9rem;">Peak ATS Score</p>
        <h2 style="margin: 5px 0 0 0; font-size: 2.2rem; color: #8B5CF6;">{stats['highest_score']}%</h2>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div style="background: rgba(18, 20, 23, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px;">
        <p style="color: #9CA3AF; margin: 0; font-size: 0.9rem;">Optimization Delta</p>
        <h2 style="margin: 5px 0 0 0; font-size: 2.2rem; color: #F59E0B;">+24.5%</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

if not history_records:
    st.info("👋 No resume analyses recorded yet. Navigate to **Upload** to scan your first resume!")
else:
    df = pd.DataFrame(history_records)
    df['created_at'] = pd.to_datetime(df['created_at'])

    col_chart1, col_chart2 = st.columns([1.2, 1])

    with col_chart1:
        st.subheader("📈 Score Progression Over Time")
        fig_trend = px.line(
            df, 
            x='created_at', 
            y=['overall_score', 'semantic_score', 'skill_score'],
            labels={'value': 'Score (%)', 'created_at': 'Date', 'variable': 'Metric'},
            color_discrete_map={
                'overall_score': '#3B82F6',
                'semantic_score': '#10B981',
                'skill_score': '#8B5CF6'
            }
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_chart2:
        st.subheader("🎯 ATS Target Score Distribution")
        fig_hist = px.histogram(
            df, 
            x="overall_score", 
            nbins=10, 
            color_discrete_sequence=['#3B82F6']
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis_title="ATS Score Range",
            yaxis_title="Count",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("📋 Recent Resume Audits")
    display_df = df[['id', 'filename', 'job_role', 'overall_score', 'semantic_score', 'skill_score', 'created_at']].copy()
    display_df.columns = ['ID', 'Filename', 'Target Role', 'Overall Score', 'Semantic Score', 'Skill Match', 'Date Analyzed']
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )