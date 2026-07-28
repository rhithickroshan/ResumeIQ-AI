# utils/gemini.py
import google.generativeai as genai
import os

class GeminiAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.enabled = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.enabled = True
            except Exception:
                self.enabled = False

    def generate_feedback(self, resume_text: str, jd_text: str) -> str:
        if not self.enabled:
            return "💡 *Gemini API Key not set. Add a free API key in Settings to unlock AI-powered resume rewrites!*"
            
        try:
            prompt = f"Act as an ATS recruiter. Give 3 bullet point improvements for this resume:\n{resume_text[:1500]}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating AI feedback: {str(e)}"

    def generate_interview_questions(self, jd_text: str) -> str:
        if not self.enabled:
            return "💡 *Gemini API Key not set. Add a free API key in Settings to unlock AI interview question generation!*"
            
        try:
            prompt = f"Generate 5 interview questions based on this job description:\n{jd_text[:1500]}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating interview questions: {str(e)}"