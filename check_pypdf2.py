import PyPDF2

pdf_path = "statement.pdf"
text = ""
with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for i in range(min(10, len(reader.pages))): # Just check first 10 pages for speed
        page = reader.pages[i]
        text += page.extract_text() + "\n"

test_codes = ['UCGRL9GE81', 'UC4RL8BO6N', 'UBH0V74V9M', 'UC20V8D8H7']
found_any = False
for c in test_codes:
    if c in text:
        print(f"PyPDF2 found {c}!")
        found_any = True
        
if not found_any:
    print("PyPDF2 didn't find them either.")
    
# Let's extract 10-char alphanumeric logic to see if ANY codes are here using pypdf2
import re
matches = re.findall(r'[A-Z0-9]{10}', text)
print(f"PyPDF2 found {len(matches)} generic 10-char codes in first 10 pages.")
if matches:
    print(matches[:10])
