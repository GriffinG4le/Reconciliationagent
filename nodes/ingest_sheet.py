import gspread
from config import SHEET_NAME_OR_URL
import os

def run(data):
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError("Missing credentials.json in the folder.")
    
    if "INSERT_YOUR" in SHEET_NAME_OR_URL:
        raise ValueError("Please update config.py with your real Google Sheet URL!")
        
    print(f"Connecting to Google Sheets...")
    gc = gspread.service_account(filename='credentials.json')
    try:
        if "spreadsheets/d/" in SHEET_NAME_OR_URL:
            sh = gc.open_by_url(SHEET_NAME_OR_URL)
        else:
            sh = gc.open(SHEET_NAME_OR_URL)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Could not find sheet. Did you share it with the service account email?")
        
    worksheet = sh.get_worksheet(0) # First tab
    
    print("Fetching records...")
    records = worksheet.get_all_records()
    
    # Store the row number so we can write back specifically to the correct cell without overwriting the whole sheet
    for idx, r in enumerate(records):
        for k in list(r.keys()):
            r[k] = str(r[k]) # Normalize
        r["_sheet_row"] = idx + 2 # row 1 is header
            
    data["sheet_records"] = records
    return data
