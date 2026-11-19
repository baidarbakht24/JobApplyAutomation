"""
Data models for Job Application Automation.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class JobListing:
    job_id: str
    title: str
    company: str
    location: str = "Remote (US)"
    employment_type: str = "Contract"  # Contract, Full-time, Part-time, Internship
    est_compensation: str = "$22 - $30/hr"
    match_score: int = 0
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    fit_summary: str = ""
    apply_url: str = ""
    source: str = "LinkedIn"
    date_added: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    status: str = "Ready to Apply"  # Ready to Apply, Applied, Interviewing, Offer, Rejected
    applied_date: str = ""
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class CandidateProfile:
    name: str = "Baidar Bakht"
    email: str = "baidarbakht24@gmail.com"
    phone: str = "412-607-6588"
    city: str = "Monroeville"
    state: str = "PA"
    zip_code: str = "15146"
    linkedin_url: str = "https://www.linkedin.com/in/baidar-bakht-a83350365/"
    university: str = "The Pennsylvania State University – Greater Allegheny"
    degree: str = "Bachelor of Science in Information Technology"
    graduation_date: str = "Fall 2026 (Expected)"
    gpa: str = "3.7"
    work_authorization_us: bool = True
    requires_sponsorship: bool = False
    years_python: int = 2
    years_excel: int = 3
    years_it_support: int = 2
    years_database: int = 2
    
    # Core Resume Keywords
    core_skills: List[str] = field(default_factory=lambda: [
        "python", "java", "excel", "data cleansing", "database hygiene",
        "software evaluation", "ams", "wild apricot", "growthzone", "glue up",
        "pos", "it support", "troubleshooting", "customer service",
        "workflow automation", "virustotal", "cybersecurity", "input validation"
    ])
