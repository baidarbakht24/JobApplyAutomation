#!/usr/bin/env python3
"""
Job Apply Automation Master Controller.
Author: Built for Baidar Bakht
Penn State IT Student | Remote Job & Contract Automation System
"""

import os
import sys
from src.models import CandidateProfile, JobListing
from src.excel_manager import ExcelTrackerManager
from src.job_searcher import LinkedInJobSearcher
from src.resume_matcher import ResumeMatcher
from src.cover_letter_generator import CoverLetterGenerator
from src.linkedin_automator import LinkedInAutomator

def print_banner():
    print("""
========================================================================
   🎯 LINKEDIN REMOTE JOB & CONTRACT AUTOMATION SYSTEM
   Candidate: Baidar Bakht | Penn State IT (GPA: 3.7)
   Target: Entry-Level IT Support, Data Hygiene, Junior Python, Cyber
========================================================================
""")

def display_jobs_table(jobs):
    print(f"\n{'ID':<12} | {'MATCH':<6} | {'TITLE':<38} | {'COMPANY':<28} | {'TYPE':<22} | {'STATUS':<15}")
    print("-" * 130)
    for j in jobs:
        print(f"{j.job_id:<12} | {j.match_score:>4}% | {j.title[:36]:<38} | {j.company[:26]:<28} | {j.employment_type[:20]:<22} | {j.status:<15}")
    print("-" * 130)

def run_pipeline(profile, tracker, matcher, generator, automator):
    print("\n" + "=" * 70)
    print("🚀 EXECUTING FULL JOB APPLICATION AUTOMATION PIPELINE")
    print("=" * 70)
    
    # 1. Ensure all seed jobs are loaded
    print("\n[Step 1/5] Loading & Verifying Targeted Remote Jobs...")
    seed_jobs = LinkedInJobSearcher.get_seed_jobs()
    for j in seed_jobs:
        tracker.add_job(j)
    print(f"   Loaded {len(tracker.jobs)} active remote jobs & contracts.")

    # 2. Re-evaluating Match Scores
    print("\n[Step 2/5] Scoring Jobs Against Baidar Bakht's Resume...")
    for j in tracker.jobs:
        analysis = matcher.analyze_job(j.title, f"{j.fit_summary} {' '.join(j.matched_skills)}")
        # Keep highest high-fidelity match
        j.match_score = max(j.match_score, analysis["score"])
        print(f"   • {j.job_id} | {j.match_score}% | {j.title[:32]} at {j.company[:22]}")

    # 3. Generating Customized Cover Letters
    print("\n[Step 3/5] Generating Customized Tailored Application Pitches...")
    os.makedirs("generated_applications", exist_ok=True)
    for j in tracker.jobs:
        path = generator.save_to_file(j)
    print(f"   Successfully generated {len(tracker.jobs)} personalized cover letters in 'generated_applications/'.")

    # 4. Synchronizing Excel & CSV Trackers
    print("\n[Step 4/5] Synchronizing Master Excel & CSV Trackers...")
    tracker.save()
    print(f"   Saved: {os.path.abspath(tracker.xlsx_path)}")
    print(f"   Saved: {os.path.abspath(tracker.csv_path)}")

    # 5. Display Pipeline Summary
    print("\n[Step 5/5] Pipeline Run Complete! Application Queue Ready:")
    display_jobs_table(tracker.jobs)
    print("=" * 70)
    print("✨ ALL JOBS EVALUATED, COVER LETTERS GENERATED, & EXCEL TRACKER SYNCHRONIZED!")
    print("=" * 70 + "\n")

def main():
    profile = CandidateProfile()
    tracker = ExcelTrackerManager()
    matcher = ResumeMatcher(profile)
    generator = CoverLetterGenerator(profile)
    automator = LinkedInAutomator(profile)

    # Check CLI arguments for non-interactive / automated batch mode
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--all", "--auto", "-a", "run"):
        print_banner()
        run_pipeline(profile, tracker, matcher, generator, automator)
        return

    # Pre-populate seed jobs if tracker is empty
    if not tracker.jobs:
        print("[Initializing] Populating tracker with curated seed remote opportunities...")
        for job in LinkedInJobSearcher.get_seed_jobs():
            tracker.add_job(job)
        tracker.save()
        print(f"[Done] Created initial tracker with {len(tracker.jobs)} targeted remote jobs.")

    while True:
        print_banner()
        print("MAIN MENU:")
        print("  [1] View & Explore Curated Remote Jobs & Contracts")
        print("  [2] Launch Assisted Easy Apply for a Job (Auto-Fill & Browser Link)")
        print("  [3] Analyze Any Job Description Against Your Resume (Skill Gap & Fit %)")
        print("  [4] Generate Tailored Cover Letter / Recruiter Pitch")
        print("  [5] Update Application Status in Excel Tracker (Applied, Interview, etc.)")
        print("  [6] View Direct LinkedIn Boolean Search URLs (Pre-filtered Remote)")
        print("  [7] Sync & Open Excel Tracker (jobs_tracker.xlsx)")
        print("  [8] Run Entire Automation Pipeline (Evaluate, Generate Letters, Sync Excel)")
        print("  [0] Exit")
        print("=" * 72)
        
        try:
            choice = input("Enter choice [0-7]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Good luck with your applications!")
            break

        if choice == "1":
            display_jobs_table(tracker.jobs)
            input("\nPress Enter to return to main menu...")

        elif choice == "2":
            display_jobs_table(tracker.jobs)
            job_id = input("\nEnter Job ID to apply (e.g., LI-REM-101): ").strip().upper()
            job = tracker.get_job(job_id)
            if not job:
                print(f"[Error] Job ID '{job_id}' not found.")
            else:
                automator.launch_assisted_apply(job)
                mark_applied = input("Did you submit or initiate the application? Mark as 'Applied'? (y/n): ").strip().lower()
                if mark_applied == 'y':
                    tracker.update_status(job_id, "Applied", "Applied via LinkedIn Easy Apply")
                    tracker.save()
                    print(f"[Updated] Status for {job_id} updated to 'Applied' in Excel tracker!")
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\n--- Analyze Job Description Against Resume ---")
            print("Paste the job title and description below (enter an empty line when done):")
            title_input = input("Job Title: ").strip()
            print("Description (paste text, then press Enter twice):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            full_text = "\n".join(lines)
            
            analysis = matcher.analyze_job(title_input, full_text)
            print("\n" + "=" * 50)
            print(f"📊 FIT ANALYSIS: {title_input}")
            print("=" * 50)
            print(f"Match Score: {analysis['score']}% ({analysis['fit_tier']})")
            print(f"\n✅ Matched Resume Strengths:")
            for m in analysis['matched_skills']:
                print(f"   • {m}")
            if analysis['missing_skills']:
                print(f"\n⚠️ Potential Skill Gaps (Be ready to address in interviews):")
                for m in analysis['missing_skills']:
                    print(f"   • {m}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            display_jobs_table(tracker.jobs)
            job_id = input("\nEnter Job ID to generate cover letter for: ").strip().upper()
            job = tracker.get_job(job_id)
            if not job:
                print(f"[Error] Job ID '{job_id}' not found.")
            else:
                letter = generator.generate_pitch(job)
                filepath = generator.save_to_file(job)
                print("\n" + "=" * 60)
                print(f"📄 TAILORED APPLICATION PITCH FOR {job.company}:")
                print("=" * 60)
                print(letter)
                print("=" * 60)
                print(f"[Saved] Letter saved to file: {filepath}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            display_jobs_table(tracker.jobs)
            job_id = input("\nEnter Job ID to update: ").strip().upper()
            job = tracker.get_job(job_id)
            if not job:
                print(f"[Error] Job ID '{job_id}' not found.")
            else:
                print("Status Options: [1] Ready to Apply  [2] Applied  [3] Interviewing  [4] Offer  [5] Rejected")
                st_choice = input("Select new status [1-5]: ").strip()
                status_map = {
                    "1": "Ready to Apply",
                    "2": "Applied",
                    "3": "Interviewing",
                    "4": "Offer",
                    "5": "Rejected"
                }
                new_status = status_map.get(st_choice, "Applied")
                notes = input("Add any notes (optional): ").strip()
                tracker.update_status(job_id, new_status, notes)
                tracker.save()
                print(f"[Success] Updated {job_id} to '{new_status}' in jobs_tracker.xlsx and jobs_tracker.csv!")
            input("\nPress Enter to continue...")

        elif choice == "6":
            print("\n" + "=" * 70)
            print("🌐 PRE-FILTERED DIRECT LINKEDIN BOOLEAN SEARCH CAMPAIGNS:")
            print("=" * 70)
            for key, camp in LinkedInJobSearcher.SEARCH_CAMPAIGNS.items():
                url = LinkedInJobSearcher.build_linkedin_url(camp["keywords"], remote=True, contract_only=camp.get("contract", False))
                print(f"\n🎯 {camp['title']}:")
                print(f"   Search Query: {camp['keywords']}")
                print(f"   Direct URL:   {url}")
            print("\n" + "=" * 70)
            input("\nPress Enter to continue...")

        elif choice == "7":
            tracker.save()
            abs_path = os.path.abspath(tracker.xlsx_path)
            print(f"\n[Excel Tracker] Saved and synchronized to:")
            print(f"   📊 Excel (.xlsx): {abs_path}")
            print(f"   📄 CSV   (.csv):  {os.path.abspath(tracker.csv_path)}")
            try:
                os.startfile(abs_path)
                print("[Launched] Opened Excel tracker in Microsoft Excel.")
            except Exception:
                print("[Info] You can open 'jobs_tracker.xlsx' directly from your Desktop/JobApplyAutomation folder.")
            input("\nPress Enter to continue...")

        elif choice == "8":
            run_pipeline(profile, tracker, matcher, generator, automator)
            input("\nPress Enter to continue...")

        elif choice == "0":
            print("\nExiting. Best of luck with your job search, Baidar!")
            break

        else:
            print("[Invalid choice] Please enter a number between 0 and 8.")

if __name__ == "__main__":
    main()
