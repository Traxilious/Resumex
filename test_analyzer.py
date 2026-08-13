import unittest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from services.ats_engine import analyze_ats_match
from services.scoring_engine import calculate_resume_score
from services.authenticity_detector import analyze_authenticity_score
from services.feedback_engine import generate_smart_feedback

class TestResumeXEngine(unittest.TestCase):

    def setUp(self):
        self.sample_cleaned_text = (
            "jeshurun nethala email jesh@gmail.com phone 9876543210 linkedin.com/in/jesh "
            "github.com/jesh summary experienced web developer skilled in python javascript html css "
            "react node.js sql git docker rest api data analysis build scalable web apps"
        )
        self.sample_parsed_data = {
            "raw_text": self.sample_cleaned_text,
            "cleaned_text": self.sample_cleaned_text,
            "word_count": 220,
            "character_count": 1400,
            "contact_info": {
                "email": "jesh@gmail.com",
                "phone": "9876543210",
                "linkedin": "linkedin.com/in/jesh",
                "github": "github.com/jesh",
                "portfolio": None
            },
            "sections": {
                "contact_info": True,
                "summary": True,
                "education": True,
                "skills": True,
                "experience": True,
                "projects": True,
                "certifications": False
            }
        }

    def test_authenticity_detection(self):
        res = analyze_authenticity_score(self.sample_cleaned_text)
        self.assertGreaterEqual(res["ai_percentage"], 70)
        self.assertEqual(res["risk_level"], "Natural Phrasing")

    def test_ats_keyword_matching(self):
        core_skills = ["javascript", "html", "css", "react", "git"]
        optional_skills = ["typescript", "vue", "docker"]
        
        ats_res = analyze_ats_match(self.sample_cleaned_text, core_skills, optional_skills)
        self.assertGreaterEqual(ats_res["ats_score"], 70)
        self.assertIn("javascript", ats_res["matched_skills"])

    def test_overall_resume_scoring(self):
        core_skills = ["javascript", "html", "css", "react", "git"]
        optional_skills = ["typescript", "vue", "docker"]
        ats_res = analyze_ats_match(self.sample_cleaned_text, core_skills, optional_skills)
        
        score_res = calculate_resume_score(self.sample_parsed_data, ats_res)
        self.assertGreaterEqual(score_res["overall_score"], 70)

if __name__ == '__main__':
    print("Running ResumeX Deep Unit Test Suite...\n")
    unittest.main()
