"""
Resume Matcher: Analyzes job descriptions against Baidar Bakht's resume.
Calculates match percentage and extracts key selling points.
"""

import re
from typing import Dict, List, Tuple
from .models import CandidateProfile

class ResumeMatcher:
    def __init__(self, profile: CandidateProfile = None):
        self.profile = profile or CandidateProfile()
        
        # Skill categories mapped to resume experiences
        self.skill_weights = {
            # IT Support & Operations
            "it support": 12, "help desk": 12, "technical support": 12, "service desk": 10,
            "troubleshooting": 10, "pos": 8, "hardware": 6, "ticketing": 8,
            # Data Hygiene & Excel
            "excel": 12, "data cleansing": 12, "database": 10, "data entry": 10,
            "auditing": 8, "duplicate": 8, "reconciliation": 8, "crm": 8, "ams": 10,
            # Scripting & Programming
            "python": 12, "java": 8, "automation": 10, "scripting": 10, "workflow": 8,
            # Security & Compliance
            "cybersecurity": 10, "security": 8, "virustotal": 8, "compliance": 8,
            # Soft Skills & Education
            "communication": 6, "problem solving": 6, "customer support": 8,
            "information technology": 8, "penn state": 4
        }

    def analyze_job(self, title: str, description: str) -> Dict:
        """
        Calculates match score (0 - 100), matched skills, missing skills, and interview tips.
        """
        text = f"{title} {description}".lower()
        
        matched = []
        missing = []
        score_accum = 0
        total_possible = 0

        # Keywords commonly found in target job posts
        target_keywords = [
            ("it support", "Hands-on IT Support & hardware/software troubleshooting"),
            ("help desk", "Customer-facing IT service desk experience"),
            ("troubleshooting", "Defensive diagnostic and problem-solving skills"),
            ("excel", "Advanced Microsoft Excel (data cleansing, auditing aging records)"),
            ("data cleansing", "Standardizing large datasets and deduplication"),
            ("database", "Database hygiene and record pruning"),
            ("python", "Python application engineering (banking simulator & automation scripts)"),
            ("java", "Academic Java object-oriented programming foundation"),
            ("automation", "Configuring automated multi-day trigger workflows"),
            ("customer service", "Customer interaction and problem-solving in fast-paced retail"),
            ("pos", "Point-of-Sale (POS) system operations and stock auditing"),
            ("cybersecurity", "Foundational cybersecurity analysis & VirusTotal"),
            ("software evaluation", "Evaluating SaaS/AMS software platforms (Wild Apricot, GrowthZone, Glue Up)")
        ]

        for kw, resume_highlight in target_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                matched.append((kw, resume_highlight))
                score_accum += self.skill_weights.get(kw, 8)
            else:
                # If the job description specifically mentions requirements we don't have
                pass

        # Check for technical requirements in description
        req_checks = [
            "sql", "aws", "azure", "linux", "active directory", "comptia",
            "networking", "powershell", "api", "git"
        ]
        for req in req_checks:
            if re.search(r'\b' + re.escape(req) + r'\b', text):
                if req not in [m[0] for m in matched]:
                    missing.append(req.title())

        # Normalize score to 100 scale
        base_match = 65  # Base match for entry-level / IT student
        if "intern" in text or "junior" in text or "entry" in text or "contract" in text:
            base_match += 10
        
        calculated_score = min(98, base_match + len(matched) * 4 - len(missing) * 2)
        calculated_score = max(50, calculated_score)

        return {
            "score": calculated_score,
            "matched_skills": [m[0].title() for m in matched],
            "resume_highlights": [m[1] for m in matched],
            "missing_skills": missing[:5],
            "fit_tier": "High Fit" if calculated_score >= 85 else ("Medium Fit" if calculated_score >= 70 else "Low Fit")
        }
