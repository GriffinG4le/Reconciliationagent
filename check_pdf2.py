import json
import sys

sys.stdout = open('check_pdf_output2.txt', 'w', encoding='utf-8')

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

test_codes = ['UCGRL9GE81', 'UC4RL8BO6N', 'UBH0V74V9M']

for row in records:
    code = get_val(row, "code").upper()
    if code in test_codes:
        amt = get_val(row, "amount")
        name = get_val(row, "name")
        print(f"--- Searching for Row: CODE={code}, AMOUNT={amt}, NAME={name} ---")
        
        # Searching by amount
        clean_amt = amt.replace(",", "").replace(".00", "")
        # Find index
        idx = pdf_text.find(clean_amt)
        if idx != -1:
            print(f"Found Amount {clean_amt}!")
            print(pdf_text[max(0, idx-100):min(len(pdf_text), idx+100)])
        else:
            # Let's try searching an amount with commas
            amt_fmt = f"{int(clean_amt):,}"
            idx2 = pdf_text.find(amt_fmt)
            if idx2 != -1:
                print(f"Found formatting Amount {amt_fmt}!")
                print(pdf_text[max(0, idx2-100):min(len(pdf_text), idx2+100)])
            else:
                print("Could not find amount in PDF either.")
