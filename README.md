# 🧠 ResumeIQ AI — Enterprise ATS Resume Analyzer

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io/)
[![Sentence Transformers](https://img.shields.io/badge/NLP-Sentence--Transformers-orange.svg)](https://www.sbert.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ResumeIQ AI** is a production-grade, AI-driven Applicant Tracking System (ATS) optimization platform. Unlike basic keyword counters, ResumeIQ AI leverages **Sentence-BERT semantic embeddings**, **spaCy NLP pipeline processing**, **TF-IDF vectorizers**, and **Google Gemini 1.5** to evaluate contextual alignment between candidate resumes and job descriptions.

---

## ✨ Features

- **Semantic Match Engine:** Evaluates contextual similarity using HuggingFace's `all-MiniLM-L6-v2` transformer model.
- **NLP Skill Extraction:** Rule-based & Named Entity Recognition (NER) pipeline via spaCy.
- **Glassmorphic SaaS UI:** Modern dark-mode interface built with Streamlit & custom CSS.
- **Skill Gap Analytics:** Highlights matching skills, missing critical requirements, and learning priorities.
- **AI Feedback & Rewrites:** Powered by Google Gemini 1.5 for executive bullet point rewrites and interview question generation.
- **SQLite Audit Trail:** Persistent analysis history, CSV/JSON data export, and aggregate performance dashboards.

---

## 🏗 Architecture & Tech Stack