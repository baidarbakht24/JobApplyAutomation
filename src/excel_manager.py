"""
Excel & CSV Application Tracker Manager.
Handles reading, writing, and updating jobs in native Excel (.xlsx) and CSV format.
Includes pure-Python fallback OpenXML generator so it runs without any pip dependencies!
"""

import os
import csv
import zipfile
import xml.sax.saxutils as saxutils
from typing import List, Dict, Optional
from datetime import datetime
from .models import JobListing

class ExcelTrackerManager:
    COLUMNS = [
        "Job ID",
        "Job Title",
        "Company",
        "Location",
        "Employment Type",
        "Est. Compensation",
        "Match Score",
        "Key Matched Skills",
        "Resume Fit Summary",
        "Application Status",
        "Date Added",
        "Date Applied",
        "LinkedIn / Application Link",
        "Notes"
    ]

    def __init__(self, xlsx_path: str = "jobs_tracker.xlsx", csv_path: str = "jobs_tracker.csv"):
        self.xlsx_path = xlsx_path
        self.csv_path = csv_path
        self.jobs: List[JobListing] = []
        self.load()

    def add_job(self, job: JobListing) -> bool:
        """Adds a job listing if not already present. Returns True if added, False if duplicate."""
        for existing in self.jobs:
            if existing.job_id == job.job_id or (
                existing.title.strip().lower() == job.title.strip().lower() and
                existing.company.strip().lower() == job.company.strip().lower()
            ):
                return False  # Duplicate
        self.jobs.append(job)
        return True

    def update_status(self, job_id: str, new_status: str, notes: str = "") -> bool:
        for job in self.jobs:
            if job.job_id == job_id:
                job.status = new_status
                if new_status.lower() == "applied" and not job.applied_date:
                    job.applied_date = datetime.now().strftime("%Y-%m-%d")
                if notes:
                    job.notes = (job.notes + " | " + notes) if job.notes else notes
                return True
        return False

    def get_job(self, job_id: str) -> Optional[JobListing]:
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None

    def load(self):
        """Loads jobs from CSV if available, or initializes empty."""
        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    self.jobs = []
                    for row in reader:
                        matched = [s.strip() for s in row.get("Key Matched Skills", "").split(",") if s.strip()]
                        raw_score = row.get("Match Score", "0").replace("%", "").strip()
                        job = JobListing(
                            job_id=row.get("Job ID", ""),
                            title=row.get("Job Title", ""),
                            company=row.get("Company", ""),
                            location=row.get("Location", "Remote (US)"),
                            employment_type=row.get("Employment Type", "Contract"),
                            est_compensation=row.get("Est. Compensation", "$25/hr"),
                            match_score=int(raw_score) if raw_score.isdigit() else 0,
                            matched_skills=matched,
                            fit_summary=row.get("Resume Fit Summary", ""),
                            status=row.get("Application Status", "Ready to Apply"),
                            date_added=row.get("Date Added", ""),
                            applied_date=row.get("Date Applied", ""),
                            apply_url=row.get("LinkedIn / Application Link", ""),
                            notes=row.get("Notes", "")
                        )
                        self.jobs.append(job)
            except Exception as e:
                print(f"[Warning] Could not load existing CSV: {e}")

    def save(self):
        """Saves current jobs list to both CSV and native Excel (.xlsx)."""
        self.save_csv()
        self.save_xlsx()

    def save_csv(self):
        try:
            with open(self.csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(self.COLUMNS)
                for job in self.jobs:
                    writer.writerow([
                        job.job_id,
                        job.title,
                        job.company,
                        job.location,
                        job.employment_type,
                        job.est_compensation,
                        f"{job.match_score}%",
                        ", ".join(job.matched_skills),
                        job.fit_summary,
                        job.status,
                        job.date_added,
                        job.applied_date,
                        job.apply_url,
                        job.notes
                    ])
        except PermissionError:
            pass

    def save_xlsx(self):
        """Generates an OpenXML .xlsx file using built-in zipfile (zero external dependencies)."""
        def esc(val):
            return saxutils.escape(str(val) if val is not None else "")

        def col_name(col_idx):
            res = ""
            while col_idx > 0:
                col_idx, rem = divmod(col_idx - 1, 26)
                res = chr(65 + rem) + res
            return res

        rows_data = []
        for job in self.jobs:
            rows_data.append([
                job.job_id,
                job.title,
                job.company,
                job.location,
                job.employment_type,
                job.est_compensation,
                f"{job.match_score}%",
                ", ".join(job.matched_skills),
                job.fit_summary,
                job.status,
                job.date_added,
                job.applied_date,
                job.apply_url,
                job.notes
            ])

        # Worksheet XML with column styling
        sheet_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
            '  <sheetViews><sheetView tabSelected="1" workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
            '  <cols>'
        ]
        # Column width definitions
        col_widths = [10, 32, 24, 18, 18, 20, 14, 30, 45, 18, 14, 14, 45, 25]
        for idx, w in enumerate(col_widths, 1):
            sheet_lines.append(f'    <col min="{idx}" max="{idx}" width="{w}" customWidth="1"/>')
        sheet_lines.append('  </cols>')
        sheet_lines.append('  <sheetData>')

        # Header Row
        r_idx = 1
        sheet_lines.append(f'    <row r="{r_idx}">')
        for c_idx, h in enumerate(self.COLUMNS, 1):
            ref = f"{col_name(c_idx)}{r_idx}"
            sheet_lines.append(f'      <c r="{ref}" s="1" t="inlineStr"><is><t>{esc(h)}</t></is></c>')
        sheet_lines.append('    </row>')

        # Data Rows
        for r in rows_data:
            r_idx += 1
            sheet_lines.append(f'    <row r="{r_idx}">')
            for c_idx, cell_val in enumerate(r, 1):
                ref = f"{col_name(c_idx)}{r_idx}"
                sheet_lines.append(f'      <c r="{ref}" s="0" t="inlineStr"><is><t>{esc(cell_val)}</t></is></c>')
            sheet_lines.append('    </row>')

        sheet_lines.append('  </sheetData>')
        sheet_lines.append(f'  <autoFilter ref="A1:{col_name(len(self.COLUMNS))}{r_idx}"/>')
        sheet_lines.append('</worksheet>')
        sheet_xml = "\n".join(sheet_lines)

        content_types_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''

        rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

        workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="LinkedIn Remote Opportunities" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>'''

        wb_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

        # Corporate Navy header styling + zebra border
        styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><name val="Segoe UI"/><sz val="10"/></font>
    <font><b/><name val="Segoe UI"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0A66C2"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="2">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
  </cellXfs>
</styleSheet>'''

        try:
            with zipfile.ZipFile(self.xlsx_path, 'w', zipfile.ZIP_DEFLATED) as z:
                z.writestr('[Content_Types].xml', content_types_xml)
                z.writestr('_rels/.rels', rels_xml)
                z.writestr('xl/workbook.xml', workbook_xml)
                z.writestr('xl/_rels/workbook.xml.rels', wb_rels_xml)
                z.writestr('xl/styles.xml', styles_xml)
                z.writestr('xl/worksheets/sheet1.xml', sheet_xml)
        except PermissionError:
            fallback_path = self.xlsx_path.replace(".xlsx", "_updated.xlsx")
            print(f"[Notice] '{self.xlsx_path}' is currently open in Excel. Saved update to '{fallback_path}'.")
            with zipfile.ZipFile(fallback_path, 'w', zipfile.ZIP_DEFLATED) as z:
                z.writestr('[Content_Types].xml', content_types_xml)
                z.writestr('_rels/.rels', rels_xml)
                z.writestr('xl/workbook.xml', workbook_xml)
                z.writestr('xl/_rels/workbook.xml.rels', wb_rels_xml)
                z.writestr('xl/styles.xml', styles_xml)
                z.writestr('xl/worksheets/sheet1.xml', sheet_xml)
