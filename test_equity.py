import pdfplumber
import re

def parse_equity_page(pdf_path, page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        words = page.extract_words()
        
        # Group words by their "top" coordinate (y-axis)
        # We will round to nearest integer to handle slight variations
        rows_by_y = {}
        for w in words:
            y = round(w['top'])
            # find if there's an existing y within 2 pixels
            matched_y = y
            for existing_y in rows_by_y.keys():
                if abs(existing_y - y) <= 2:
                    matched_y = existing_y
                    break
            
            if matched_y not in rows_by_y:
                rows_by_y[matched_y] = []
            rows_by_y[matched_y].append(w)
            
        # Sort rows top to bottom
        sorted_y = sorted(rows_by_y.keys())
        
        records = []
        for y in sorted_y:
            row_words = rows_by_y[y]
            # sort words left to right
            row_words.sort(key=lambda w: w['x0'])
            row_text = " ".join([w['text'] for w in row_words])
            
            # Look for an M-Pesa code in the row
            match = re.search(r'\b([A-Z0-9]{10})\b', row_text)
            if match:
                code = match.group(1)
                
                # In Equity statements, the Credit (Paid In) is usually near the right side before the balance
                # Let's print the row to see
                print(f"Y={y} | {row_text}")

if __name__ == "__main__":
    parse_equity_page("statement.pdf", 9) # Page 10 is index 9
