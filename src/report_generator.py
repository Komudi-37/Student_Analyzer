from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_report(name, dept, sem, avg, rec_career):
    try:
        # Ensure directory exists
        os.makedirs("reports/student_reports", exist_ok=True)
        file_path = f"reports/student_reports/{name}_report.pdf"

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, 800, "Student Performance Report")

        # Student details
        c.setFont("Helvetica", 12)
        c.drawString(100, 760, f"Name: {name}")
        c.drawString(100, 740, f"Department: {dept}")
        c.drawString(100, 720, f"Semester: {sem}")
        c.line(100, 710, 500, 710)

        # Performance
        c.drawString(100, 690, f"Average Marks: {avg:.2f}")
        c.drawString(100, 670, f"Recommended Career Path: {rec_career}")

        # Footer with date
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(100, 100, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        # Save
        c.save()
        print(f"📄 Report generated successfully for {name}: {file_path}")

    except Exception as e:
        print(f"⚠️ Error generating report for {name}: {e}")
