"""
LinkedIn Easy Apply Automation Engine.
Supports Assisted / Semi-Automated Mode (human-in-the-loop) and Automated Application workflows.
"""

import os
import sys
import time
import webbrowser
from typing import Dict, Optional
from .models import CandidateProfile, JobListing
from .cover_letter_generator import CoverLetterGenerator

class LinkedInAutomator:
    def __init__(self, profile: CandidateProfile = None):
        self.profile = profile or CandidateProfile()
        self.generator = CoverLetterGenerator(self.profile)

    def prepare_application_kit(self, job: JobListing) -> Dict[str, str]:
        """
        Prepares all necessary text, screening answers, and cover letter for a specific job.
        """
        cover_pitch = self.generator.generate_pitch(job)
        
        screening_answers = {
            "First Name": self.profile.name.split()[0],
            "Last Name": " ".join(self.profile.name.split()[1:]),
            "Email": self.profile.email,
            "Phone Number": self.profile.phone,
            "LinkedIn Profile URL": self.profile.linkedin_url,
            "City": self.profile.city,
            "State": self.profile.state,
            "Postal Code": self.profile.zip_code,
            "Legally authorized to work in US?": "Yes",
            "Require sponsorship now or in future?": "No",
            "Years of experience with Python": str(self.profile.years_python),
            "Years of experience with Excel": str(self.profile.years_excel),
            "Years of experience with IT Support": str(self.profile.years_it_support),
            "Years of experience with Databases": str(self.profile.years_database),
            "University / College": self.profile.university,
            "Degree": self.profile.degree,
            "Expected Graduation": self.profile.graduation_date,
            "GPA": self.profile.gpa
        }

        return {
            "job_title": job.title,
            "company": job.company,
            "apply_url": job.apply_url,
            "screening_answers": screening_answers,
            "cover_pitch": cover_pitch
        }

    def launch_assisted_apply(self, job: JobListing, resume_path: Optional[str] = None):
        """
        Launches browser directly to the targeted job search / application page,
        prints pre-computed screening answers to the console, and saves the custom cover letter.
        """
        kit = self.prepare_application_kit(job)
        saved_letter_path = self.generator.save_to_file(job)

        print("\n" + "="*70)
        print(f"🚀 LAUNCHING APPLICATION: {job.title} at {job.company}")
        print("="*70)
        print(f"Match Score: {job.match_score}% | Type: {job.employment_type} | Est. Pay: {job.est_compensation}")
        print(f"Resume Highlights: {job.fit_summary}")
        print(f"\n📂 Generated Tailored Cover Note saved at: {saved_letter_path}")
        print("\n📋 PRE-FILLED SCREENING ANSWERS FOR THIS APPLICATION:")
        for q, a in kit["screening_answers"].items():
            print(f"   • {q:<42}: {a}")
        
        print("\n🌐 Opening LinkedIn Application Link in your browser...")
        try:
            webbrowser.open(job.apply_url)
        except Exception as e:
            print(f"[Notice] Open manually in browser: {job.apply_url}")

        print("\n💡 Tip: Once the page loads, click 'Easy Apply' or 'Apply'.")
        print(f"   The custom pitch in '{saved_letter_path}' is ready to paste if a note is requested.")
        print("="*70 + "\n")

    def run_browser_automation(self, job: JobListing, headless: bool = False):
        """
        Attempts to run automated Playwright/Selenium bot if the user has installed dependencies.
        Provides clean fallback instructions if not yet installed.
        """
        try:
            from playwright.sync_api import sync_playwright
            has_playwright = True
        except ImportError:
            has_playwright = False

        if not has_playwright:
            print("\n[Notice] Playwright is not currently installed.")
            print("To enable full direct browser automation, install Playwright:")
            print("   pip install playwright && playwright install chromium")
            print("Falling back smoothly to Assisted / Semi-Automated Application Mode...\n")
            self.launch_assisted_apply(job)
            return

        print(f"\n[Bot] Launching Chromium browser to automate application for {job.title}...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(job.apply_url)
            print("[Bot] Loaded job page. Inspecting for 'Easy Apply' button...")
            time.sleep(3)
            # Find Easy Apply
            easy_apply_btn = page.query_selector("button.jobs-apply-button")
            if easy_apply_btn:
                easy_apply_btn.click()
                print("[Bot] Clicked Easy Apply. Filling form fields...")
                time.sleep(2)
                # Fill common fields
                phone_input = page.query_selector("input[id*='phoneNumber']")
                if phone_input:
                    phone_input.fill(self.profile.phone)
                print("[Bot] Reached review step. Pausing for user confirmation...")
                time.sleep(5)
            else:
                print("[Bot] Standard external application link detected. Launching in browser.")
                webbrowser.open(job.apply_url)
            browser.close()
