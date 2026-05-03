import json
import sys

# output to a healthy utf-8 file
sys.stdout = open('check_pdf_output.txt', 'w', encoding='utf-8')

STATE_FILE = "pipeline_state.json"
with open(STATE_FILE, "r") as f:
    state = json.load(f)

pdf_text = state.get("data", {}).get("pdf_text", "")
records = state.get("data", {}).get("sheet_records", [])

def get_val(row, target_key):
    for k, v in row.items():
        if str(k).strip().lower() == target_key.lower():
            return str(v).strip()
    return ""

found = 0
not_found = []

for row in records:
    # Use exact same logic
    code = get_val(row, "code").upper()
    if code and code != "NAN":
        if code in pdf_text:
            found += 1
        else:
            not_found.append(code)

print(f"Tested {found + len(not_found)} codes.")
print(f"Found exactly in pdf_text: {found}")
if not_found:
    print(f"First 5 NOT FOUND codes: {not_found[:5]}")
    
    # Try finding with stripped text
    stripped_pdf = pdf_text.replace(" ", "").replace("\n", "").replace("\xa0", "")
    found_stripped = 0
    for c in not_found:
        if c in stripped_pdf:
            found_stripped += 1
            
    print(f"Out of {len(not_found)} not found, found {found_stripped} in completely stripped PDF text.")
