import unittest
import os
from services.document_parser import parse_document
from services.ats_engine import analyze_ats_match
from services.scoring_engine import calculate_resume_score
from services.authenticity_detector import analyze_authenticity_score
from services.feedback_engine import generate_smart_feedback

class TestResumeXEngine(unittest.TestCase):

    def setUp(self):
        self.sample_resume = """
        Jeshurun Alex
        Email: jeshurun@example.com | Phone: +1-555-019-2831
        LinkedIn: linkedin.com/in/jeshurun | GitHub: github.com/jeshurun

        PROFESSIONAL SUMMARY
        Experienced Web Developer with 3+ years of expertise building scalable web applications, REST APIs, and responsive frontends.

        TECHNICAL SKILLS
        Languages & Frameworks: JavaScript, HTML, CSS, React, Node.js, Python, SQL, Git, Docker, REST API.

        PROJECTS
        Full Stack E-Commerce Platform
        - Developed responsive React frontend and Node.js REST API backend.
        - Integrated PostgreSQL database and deployed using Docker containers.

        EDUCATION
        B.S. in Computer Science - State University
        """

    def test_ats_matching(self):
        core_skills = ["javascript", "html", "css", "react", "git", "node.js", "rest api"]
        optional_skills = ["typescript", "vue", "docker", "tailwind"]
        
        res = analyze_ats_match(self.sample_resume.lower(), core_skills, optional_skills)
        self.assertGreaterEqual(res["ats_score"], 70)
        self.assertIn("react", res["matched_skills"])

    def test_authenticity_detection(self):
        res = analyze_authenticity_score(self.sample_resume)
        self.assertLess(res["ai_percentage"], 30)
        self.assertEqual(res["risk_level"], "Natural Phrasing")

    def test_deep_analysis(self):
        parsed = {
            "cleaned_text": self.sample_resume.lower(),
            "raw_text": self.sample_resume,
            "word_count": len(self.sample_resume.split()),
            "contact_info": {
                "email": "jeshurun@example.com",
                "phone": "+1-555-019-2831",
                "linkedin": "linkedin.com/in/jeshurun",
                "github": "github.com/jeshurun",
                "portfolio": None
            },
            "sections": {"summary": 1, "experience": 1, "projects": 1, "education": 1, "skills": 1}
        }
        ats = analyze_ats_match(self.sample_resume.lower(), ["javascript", "react", "python"], ["docker"])
        score = calculate_resume_score(parsed, ats)
        authenticity = analyze_authenticity_score(self.sample_resume)
        feedback = generate_smart_feedback(parsed, ats, score, authenticity, "Web Developer")

        self.assertGreaterEqual(score["overall_score"], 50)
        self.assertIn("pros", feedback)
        self.assertIn("cons", feedback)

if __name__ == '__main__':
    print("Running ResumeX Deep Unit Test Suite...\n")
    unittest.main()
