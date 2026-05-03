import json
import re
import sys

sys.stdout = open('check_pdf_output3.txt', 'w', encoding='utf-8')

STATE_FILE = "pipeline_state.json"
with open(STATE_FILE, "r") as f:
    state = json.load(f)

pdf_text = state.get("data", {}).get("pdf_text", "")
records = state.get("data", {}).get("sheet_records", [])

def canonicalize(text):
    text = text.upper()
    mapping = {'O': '0', 'I': '1', 'L': '1', 'S': '5', 'B': '8', 'Z': '2', 'A': '4'}
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text

stripped_pdf = re.sub(r'\s+', '', pdf_text)
canonical_pdf = canonicalize(stripped_pdf)

def get_val(row, target_key):
    for k, v in row.items():
        if str(k).strip().lower() == target_key.lower():
            return str(v).strip()
    return ""

found = 0
not_found = []

for row in records:
    code = get_val(row, "code").upper()
    if code and code != "NAN":
        canonical_code = canonicalize(code)
        if canonical_code in canonical_pdf:
            found += 1
        else:
            not_found.append(code)

print(f"Tested {found + len(not_found)} codes using OCR normalization.")
print(f"Found exactly in normalized PDF: {found}")
if not_found:
    print(f"NOT FOUND (even with OCR norm): {not_found[:5]}")
