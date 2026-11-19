"""
Cover Letter & Application Pitch Generator.
Generates tailored, high-converting outreach notes and cover letters.
"""

import os
from .models import CandidateProfile, JobListing

class CoverLetterGenerator:
    def __init__(self, profile: CandidateProfile = None):
        self.profile = profile or CandidateProfile()

    def generate_pitch(self, job: JobListing, tone: str = "professional") -> str:
        """
        Generates a quick LinkedIn message / pitch note (under 150 words)
        ideal for Easy Apply cover note or recruiter outreach.
        """
        title_lower = job.title.lower()

        if "python" in title_lower or "developer" in title_lower or "software" in title_lower:
            hook = (
                f"I am writing to express my strong enthusiasm for the {job.title} position at {job.company}. "
                f"As an Information Technology student at Penn State with practical experience building defensive Python "
                f"simulations (including real-time transaction processing, error handling, and API/logic workflows), "
                f"I specialize in writing clean, reliable code and building automated solutions."
            )
            highlights = (
                "• Engineered a multi-feature Python banking simulator with PIN authentication and input validation.\n"
                "• Designed automated workflow notification triggers reducing administrative overhead.\n"
                "• Strong grasp of software evaluation, sandbox testing, and database integrity."
            )
        elif "data" in title_lower or "cleansing" in title_lower or "database" in title_lower:
            hook = (
                f"I am eager to apply for the {job.title} role at {job.company}. "
                f"During my IT Internship at the Mon Yough Area Chamber of Commerce, my primary focus was cleaning, "
                f"auditing, and standardizing large datasets in Microsoft Excel, eliminating duplicate records, "
                f"and restoring full database integrity across membership management platforms."
            )
            highlights = (
                "• Cleaned and audited hundreds of aging invoice records and duplicate accounts in Excel.\n"
                "• Evaluated and prepared datasets for migration across modern AMS platforms (Wild Apricot, Glue Up).\n"
                "• Configured recurring automated triggers to eliminate manual data upkeep."
            )
        elif "cyber" in title_lower or "security" in title_lower or "soc" in title_lower:
            hook = (
                f"I am excited to apply for the {job.title} position at {job.company}. "
                f"Currently pursuing my B.S. in Information Technology at Penn State (3.7 GPA), I have focused on "
                f"foundational cybersecurity analysis, threat verification with tools like VirusTotal, "
                f"and secure input validation practices to safeguard organizational data."
            )
            highlights = (
                "• Practical knowledge of threat indicators, OSINT verification (VirusTotal), and security posture.\n"
                "• Experience pruning inactive accounts and securing database records during system migrations.\n"
                "• Maintained 3.7 GPA on Dean's List while balancing hands-on technical internships."
            )
        else:  # IT Support / Help Desk / Technical Support
            hook = (
                f"I am thrilled to submit my application for the {job.title} role at {job.company}. "
                f"Combining my academic training in Information Technology at Penn State with hands-on IT internship "
                f"experience and fast-paced customer-facing POS troubleshooting, I bring both technical diagnostic skill "
                f"and active listening to deliver high first-contact resolution rates."
            )
            highlights = (
                "• Performed software platform evaluations, sandbox trials, and user onboarding.\n"
                "• Handled daily POS, hardware, and inventory management software troubleshooting in retail operations.\n"
                "• Configured automated alert sequences and audited customer/member data records in Excel."
            )

        letter = f"""Dear {job.company} Hiring Team,

{hook}

Key contributions I would bring to your team include:
{highlights}

I am located in Pennsylvania (EST), available immediately for remote work/contracts, and fully authorized to work in the US without requiring sponsorship.

Thank you for your time and consideration. I welcome the opportunity to discuss how my skill set can support {job.company}'s goals.

Sincerely,

{self.profile.name}
{self.profile.phone} | {self.profile.email}
LinkedIn: {self.profile.linkedin_url}
Penn State University – B.S. in Information Technology (GPA: 3.7)
"""
        return letter

    def save_to_file(self, job: JobListing, output_dir: str = "generated_applications") -> str:
        os.makedirs(output_dir, exist_ok=True)
        safe_company = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in job.company).replace(" ", "_")
        filename = f"Application_{safe_company}_{job.job_id}.txt"
        file_path = os.path.join(output_dir, filename)
        content = self.generate_pitch(job)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path
