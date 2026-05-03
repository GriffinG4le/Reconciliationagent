import re
import difflib

def get_val(row, target_key):
    for k, v in row.items():
        if str(k).strip().lower() == target_key.lower():
            return str(v).strip()
    return ""

def canonicalize(text):
    text = text.upper()
    mapping = {
        'O': '0', 'I': '1', 'L': '1', 
        'S': '5', 'B': '8', 'Z': '2', 'A': '4'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text

def find_best_match(target_code, extracted_codes, canonical_codes_map):
    # 1. Exact Match
    if target_code in extracted_codes:
        return target_code, "Exact"
        
    # 2. Canonical (OCR Error) Match
    target_canon = canonicalize(target_code)
    for raw_code, canon_code in canonical_codes_map.items():
        if target_canon == canon_code:
            return raw_code, "OCR Corrected"
            
    # 3. Fuzzy Match (1 character difference)
    matches = difflib.get_close_matches(target_code, extracted_codes, n=1, cutoff=0.85)
    if matches:
        return matches[0], "Fuzzy"
        
    return None, None

def parse_amount(amt_str):
    if not amt_str or amt_str.lower() == "nan":
        return 0.0
    try:
        return float(amt_str.replace(",", ""))
    except ValueError:
        return 0.0

def run(data):
    records = data.get("sheet_records", [])
    pdf_records = data.get("pdf_records", [])
    
    extracted_codes = [rec["code"] for rec in pdf_records]
    canonical_codes_map = {code: canonicalize(code) for code in extracted_codes}
    pdf_records_map = {rec["code"]: rec for rec in pdf_records}
    
    for row in records:
        code = get_val(row, "code").upper()
        amount = get_val(row, "amount")
        current_status = get_val(row, "status")
        
        if code and code != "NAN":
            matched_code, match_type = find_best_match(code, extracted_codes, canonical_codes_map)
            
            if matched_code:
                matched_record = pdf_records_map[matched_code]
                actual_amount = matched_record["paid_in"] if parse_amount(matched_record["paid_in"]) > 0 else matched_record["withdrawn"]
                
                if not amount or str(amount).lower() == "nan":
                    row["Amount_UPDATE"] = actual_amount
                    if match_type == "Exact":
                        row["Status_UPDATE"] = "Auto-filled Amount [Exact]"
                    else:
                        row["Status_UPDATE"] = f"Auto-filled Amount [{match_type}]"
                        row["Accurate_Code_UPDATE"] = matched_code
                else:
                    claimed_amt_val = parse_amount(amount)
                    paid_in_val = parse_amount(matched_record["paid_in"])
                    withdrawn_val = parse_amount(matched_record["withdrawn"])
                    
                    if claimed_amt_val > 0 and (claimed_amt_val == paid_in_val or claimed_amt_val == withdrawn_val):
                        if match_type == "Exact":
                            row["Status_UPDATE"] = "Confirmed"
                        else:
                            row["Status_UPDATE"] = f"Confirmed [{match_type}]"
                            row["Accurate_Code_UPDATE"] = matched_code
                    else:
                        row["Status_UPDATE"] = f"Code Found [{match_type}]; Amount ({amount}) Mismatch (Actual: {actual_amount})"
                        if match_type != "Exact":
                            row["Accurate_Code_UPDATE"] = matched_code
            else:
                if current_status != "Approved":
                    row["Status_UPDATE"] = "Code Not Found in PDF"
                else:
                    row["Status_UPDATE"] = "Approved (Code Not Found)"
                    
    data["reconciled_records"] = records
    return data
