import pdfplumber

def scan_pdf_tables(pdf_path):
    output = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for j, table in enumerate(tables):
                    if table and len(table) > 0:
                        # Add page number and header row
                        header = [str(col).replace('\n', ' ') for col in table[0]]
                        output.append(f"Page {i+1}, Table {j} Header: {header}")
                        # Add first data row as example
                        if len(table) > 1:
                            data_row = [str(col).replace('\n', ' ') for col in table[1]]
                            output.append(f"    Example Row: {data_row}")
                            
    with open("table_structures.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(output))
        
if __name__ == "__main__":
    scan_pdf_tables("statement.pdf")
