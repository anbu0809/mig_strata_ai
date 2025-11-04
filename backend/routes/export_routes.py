from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import json
import os
import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

router = APIRouter()

@router.get("/json")
async def export_json():
    # Check if validation report exists
    if not os.path.exists("artifacts/validation_report.json"):
        return {"error": "Validation report not found"}
    
    return FileResponse(
        "artifacts/validation_report.json",
        media_type="application/json",
        filename="validation_report.json"
    )

@router.get("/xlsx")
async def export_xlsx():
    # Check if validation report exists
    if not os.path.exists("artifacts/validation_report.json"):
        return {"error": "Validation report not found"}
    
    # Load validation report
    with open("artifacts/validation_report.json", "r") as f:
        data = json.load(f)
    
    # Create Excel file
    excel_filename = "artifacts/validation_report.xlsx"
    workbook = xlsxwriter.Workbook(excel_filename)
    worksheet = workbook.add_worksheet()
    
    # Write headers
    headers = ["Category", "Status", "Error Details", "Suggested Fix", "Confidence Score"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Write data
    for row, item in enumerate(data, start=1):
        worksheet.write(row, 0, item.get("category", ""))
        worksheet.write(row, 1, item.get("status", ""))
        worksheet.write(row, 2, item.get("errorDetails", ""))
        worksheet.write(row, 3, item.get("suggestedFix", ""))
        worksheet.write(row, 4, item.get("confidenceScore", ""))
    
    workbook.close()
    
    return FileResponse(
        excel_filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="validation_report.xlsx"
    )

@router.get("/pdf")
async def export_pdf():
    # Check if validation report exists
    if not os.path.exists("artifacts/validation_report.json"):
        return {"error": "Validation report not found"}
    
    # Load validation report
    with open("artifacts/validation_report.json", "r") as f:
        data = json.load(f)
    
    # Create PDF file
    pdf_filename = "artifacts/validation_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Strata - Validation Report", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add each validation item
    for item in data:
        category = Paragraph(f"<b>{item.get('category', '')}</b>", styles["Heading2"])
        story.append(category)
        
        status = Paragraph(f"Status: {item.get('status', '')}", styles["Normal"])
        story.append(status)
        
        if item.get('errorDetails'):
            error = Paragraph(f"Error: {item.get('errorDetails', '')}", styles["Normal"])
            story.append(error)
            
        if item.get('suggestedFix'):
            fix = Paragraph(f"Suggested Fix: {item.get('suggestedFix', '')}", styles["Normal"])
            story.append(fix)
            
        score = Paragraph(f"Confidence Score: {item.get('confidenceScore', '')}", styles["Normal"])
        story.append(score)
        
        story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    
    return FileResponse(
        pdf_filename,
        media_type="application/pdf",
        filename="validation_report.pdf"
    )