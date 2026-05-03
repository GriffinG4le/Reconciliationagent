import pdfplumber
import os
import re

def run(data):
    pdf_path = "statement.pdf"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find statement PDF at {pdf_path}. Please place it here.")
        
    pdf_records = []
    
    print("Running tabular extraction on PDF...")
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 5:
                        continue
                    
                    code = str(row[0]).strip()
                    # M-Pesa codes are exactly 10 uppercase alphanumeric characters
                    if re.match(r'^[A-Z0-9]{10}$', code):
                        # Ensure we handle potential missing columns gracefully
                        paid_in = str(row[4]).strip().replace(",", "") if len(row) > 4 and row[4] else "0.00"
                        withdrawn = str(row[5]).strip().replace(",", "") if len(row) > 5 and row[5] else "0.00"
                        
                        pdf_records.append({
                            "code": code,
                            "paid_in": paid_in,
                            "withdrawn": withdrawn
                        })
                        
    data["pdf_records"] = pdf_records
    print(f"Extracted {len(pdf_records)} transactions from PDF.")
    return data
