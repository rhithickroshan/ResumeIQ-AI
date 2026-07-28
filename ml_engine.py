import spacy
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import re

class MLResumeEngine:
    def __init__(self):
        # Load models locally (singleton pattern for Streamlit caching recommended in prod)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
            
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def clean_text(self, text: str) -> str:
        """Removes special characters, URLs, and normalizes text."""
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)

    def extract_skills(self, text: str, skill_db: list) -> list:
        """Extracts skills using rule-based NLP matching."""
        doc = self.nlp(text.lower())
        found_skills = set()
        text_lower = text.lower()
        for skill in skill_db:
            if skill.lower() in text_lower:
                found_skills.add(skill)
        return list(found_skills)

    def calculate_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculates deep semantic matching using BERT embeddings."""
        embeddings1 = self.encoder.encode(self.clean_text(resume_text), convert_to_tensor=True)
        embeddings2 = self.encoder.encode(self.clean_text(jd_text), convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        return float(cosine_scores[0][0]) * 100

    def generate_ats_score(self, resume: str, jd: str, base_skills: list) -> dict:
        """Aggregates multiple ML metrics into a final production ATS Score."""
        sim_score = self.calculate_semantic_similarity(resume, jd)
        
        resume_skills = self.extract_skills(resume, base_skills)
        jd_skills = self.extract_skills(jd, base_skills)
        
        # Skill matching ratio
        if not jd_skills:
            skill_score = 100.0
        else:
            matched = set(resume_skills).intersection(set(jd_skills))
            skill_score = (len(matched) / len(jd_skills)) * 100

        # Weighted final score (60% semantic meaning, 40% hard skill matching)
        final_score = (sim_score * 0.6) + (skill_score * 0.4)
        
        return {
            "overall_score": round(final_score, 1),
            "semantic_score": round(sim_score, 1),
            "skill_match_score": round(skill_score, 1),
            "matched_skills": list(set(resume_skills).intersection(set(jd_skills))),
            "missing_skills": list(set(jd_skills) - set(resume_skills))
        }