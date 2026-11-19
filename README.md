# 🎯 LinkedIn Remote Job & Contract Automation System

Custom-engineered for **Baidar Bakht**  
B.S. in Information Technology, Penn State University (GPA: 3.7)

---

## 📌 What's Included

1. **📊 Pre-Populated Excel Tracker (`jobs_tracker.xlsx` & `jobs_tracker.csv`)**:
   - 12 curated, high-match remote jobs and contracts matching your resume across 5 domains:
     - **Remote IT Support Specialist / Help Desk Tier 1**
     - **Data Hygiene, Cleansing & Excel Specialist**
     - **Junior Python Developer & Automation Scripting**
     - **AMS & Membership Systems Coordinator (Wild Apricot, GrowthZone, Glue Up)**
     - **Junior Cybersecurity & SOC Operations Analyst**
   - Contains columns for **Job Title, Company, Location, Compensation, Match Score (%), Key Matched Skills, Resume Highlights, Application Status, Direct Links, and Notes**.
   - Includes auto-filters, frozen header rows, and corporate navy styling.

2. **⚙️ Python Job Application Automation Tool (`run.py` & `src/`)**:
   - **Interactive CLI Dashboard**: Search, analyze, track, and apply directly from your terminal.
   - **Assisted Easy Apply Engine (`src/linkedin_automator.py`)**: Launches targeted job links in your browser, pre-calculates and displays answers to common screening questions (work authorization, experience years, education), and copies your tailored application note to paste instantly.
   - **Resume Fit & Gap Analyzer (`src/resume_matcher.py`)**: Paste any job description to instantly get a 0–100% match score, list of matching resume bullets, and potential gap areas to prepare for interviews.
   - **Dynamic Cover Letter Generator (`src/cover_letter_generator.py`)**: Automatically drafts tailored application pitches highlighting your exact Chamber of Commerce internship, Python banking simulator project, or retail POS troubleshooting.
   - **Central Configuration (`config.yaml`)**: Easily adjust your personal details, screening defaults, target roles, and automation speed.

---

## 🚀 Quick Start Guide

### 1. View & Open Your Excel Tracker
Double click `jobs_tracker.xlsx` directly on your Desktop, or open it in Excel, Google Sheets, or LibreOffice.

### 2. Run the Automation Dashboard
Open PowerShell or your command prompt in this directory and run:

```bash
python run.py
```

You will see the interactive menu:
```text
========================================================================
   🎯 LINKEDIN REMOTE JOB & CONTRACT AUTOMATION SYSTEM
   Candidate: Baidar Bakht | Penn State IT (GPA: 3.7)
========================================================================
MAIN MENU:
  [1] View & Explore Curated Remote Jobs & Contracts
  [2] Launch Assisted Easy Apply for a Job (Auto-Fill & Browser Link)
  [3] Analyze Any Job Description Against Your Resume (Skill Gap & Fit %)
  [4] Generate Tailored Cover Letter / Recruiter Pitch
  [5] Update Application Status in Excel Tracker (Applied, Interview, etc.)
  [6] View Direct LinkedIn Boolean Search URLs (Pre-filtered Remote)
  [7] Sync & Open Excel Tracker (jobs_tracker.xlsx)
  [0] Exit
```

---

## 🛠️ Project Structure

```text
JobApplyAutomation/
├── README.md                          # Documentation & quick start guide
├── requirements.txt                   # Optional dependencies (playwright, beautifulsoup4)
├── config.yaml                        # User profile, screening question answers, & settings
├── run.py                             # Interactive CLI launcher
├── jobs_tracker.xlsx                  # Master Excel application tracker
├── jobs_tracker.csv                   # CSV synchronization mirror
├── generated_applications/            # Output folder for generated cover letters / pitches
└── src/
    ├── __init__.py
    ├── models.py                      # Data models for candidates, jobs, and applications
    ├── resume_matcher.py              # NLP & keyword scoring engine (0-100% fit score)
    ├── cover_letter_generator.py      # Role-specific cover letter and outreach generator
    ├── excel_manager.py               # Pure-Python OpenXML spreadsheet engine
    ├── job_searcher.py                # LinkedIn pre-filtered Boolean query generator
    └── linkedin_automator.py          # Assisted & direct browser automation runner
```

---

## 📋 Pre-Configured Screening Answers

When applying on LinkedIn Easy Apply, the automator pre-loads these answers based on your resume:

| Screening Question | Pre-Configured Answer |
| :--- | :--- |
| **Are you legally authorized to work in the US?** | Yes |
| **Will you now or in the future require visa sponsorship?** | No |
| **Years of experience with Microsoft Excel?** | 3 years (Data cleansing, duplicate resolution, aging invoices) |
| **Years of experience with Python?** | 2 years (ATM Simulator, defensive error handling, logic flows) |
| **Years of experience with IT / Technical Support?** | 2 years (AMS software evaluation, retail POS, user troubleshooting) |
| **Highest Level of Education?** | Bachelor of Science in Information Technology (Penn State, GPA 3.7) |
| **Graduation Date?** | Fall 2026 (Expected) |

---

## 💡 Recommended Next Steps
- Run `python run.py`, select option `[1]` to review the 12 curated jobs.
- Select option `[2]` to launch your first Easy Apply application.
- Select option `[6]` to open live pre-filtered LinkedIn search feeds for newly posted remote contracts in the past 24 hours.
