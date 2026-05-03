import gspread
from config import SHEET_NAME_OR_URL

def run(data):
    records = data.get("reconciled_records", [])
    if not records:
        return data
        
    gc = gspread.service_account(filename='credentials.json')
    if "spreadsheets/d/" in SHEET_NAME_OR_URL:
        sh = gc.open_by_url(SHEET_NAME_OR_URL)
    else:
        sh = gc.open(SHEET_NAME_OR_URL)
        
    worksheet = sh.get_worksheet(0)
    
    raw_headers = worksheet.row_values(1)
    headers = [str(h).strip().lower() for h in raw_headers]
    
    cells_to_update = []
    
    # Ensure Status column exists
    if "status" not in headers:
        status_col_idx = len(headers) + 1
        cells_to_update.append(gspread.Cell(row=1, col=status_col_idx, value="Status"))
        headers.append("status")
        print("Appended 'Status' column to headers.")
    else:
        status_col_idx = headers.index("status") + 1
        
    # Ensure ACCURATE CODE column exists
    if "accurate code" not in headers:
        accurate_code_col_idx = len(headers) + 1
        cells_to_update.append(gspread.Cell(row=1, col=accurate_code_col_idx, value="ACCURATE CODE"))
        headers.append("accurate code")
        print("Appended 'ACCURATE CODE' column to headers.")
    else:
        accurate_code_col_idx = headers.index("accurate code") + 1
    
    amount_col_idx = None
    if "amount" in headers:
        amount_col_idx = headers.index("amount") + 1
    
    print("Preparing batch update for Google Sheets...")
    for row in records:
        row_idx = row.get("_sheet_row")
        if not row_idx:
            continue
            
        status_to_push = row.get("Status_UPDATE")
        if status_to_push:
            cells_to_update.append(
                gspread.Cell(row=row_idx, col=status_col_idx, value=status_to_push)
            )
            
        accurate_code = row.get("Accurate_Code_UPDATE")
        if accurate_code:
            cells_to_update.append(
                gspread.Cell(row=row_idx, col=accurate_code_col_idx, value=accurate_code)
            )
            
        amount_to_push = row.get("Amount_UPDATE")
        if amount_to_push and amount_col_idx:
            cells_to_update.append(
                gspread.Cell(row=row_idx, col=amount_col_idx, value=amount_to_push)
            )
                
    if cells_to_update:
        worksheet.update_cells(cells_to_update)
        print(f"Successfully pushed {len(cells_to_update)} status updates back to the live Google Sheet!")
    else:
        print("No new statuses to push to the Sheet.")
    
    return data
