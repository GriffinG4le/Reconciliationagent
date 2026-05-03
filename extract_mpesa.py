import re

def extract_mpesa_code(text):
    """
    Extract the first 10-character alphanumeric string consisting of 
    entirely uppercase letters and numbers from the given text.
    
    Args:
        text (str): The input string to search
        
    Returns:
        str: The first matching M-Pesa code (10 uppercase alphanumeric chars)
        None: If no match is found
    """
    match = re.search(r'[A-Z0-9]{10}', text)
    if match:
        return match.group()
    return None


# Test cases
if __name__ == "__main__":
    # Test 1: Valid M-Pesa code at the beginning
    test1 = "ABC1234567X some other text"
    result1 = extract_mpesa_code(test1)
    print(f"Test 1: '{test1}' -> {result1}")
    assert result1 == "ABC1234567", f"Expected 'ABC1234567', got '{result1}'"
    
    # Test 2: Valid M-Pesa code in the middle
    test2 = "Transaction code: XYZ9876543 processed"
    result2 = extract_mpesa_code(test2)
    print(f"Test 2: '{test2}' -> {result2}")
    assert result2 == "XYZ9876543", f"Expected 'XYZ9876543', got '{result2}'"
    
    # Test 3: No valid M-Pesa code (lowercase letters)
    test3 = "This is abc1234567x with lowercase"
    result3 = extract_mpesa_code(test3)
    print(f"Test 3: '{test3}' -> {result3}")
    assert result3 is None, f"Expected None, got '{result3}'"
    
    # Test 4: No valid M-Pesa code (too short)
    test4 = "Code ABC12345 is only 9 chars"
    result4 = extract_mpesa_code(test4)
    print(f"Test 4: '{test4}' -> {result4}")
    assert result4 is None, f"Expected None, got '{result4}'"
    
    # Test 5: Multiple codes, should return the first
    test5 = "First: AAAA111111 Second: BBBB222222"
    result5 = extract_mpesa_code(test5)
    print(f"Test 5: '{test5}' -> {result5}")
    assert result5 == "AAAA111111", f"Expected 'AAAA111111', got '{result5}'"
    
    # Test 6: Empty string
    test6 = ""
    result6 = extract_mpesa_code(test6)
    print(f"Test 6: '{test6}' -> {result6}")
    assert result6 is None, f"Expected None, got '{result6}'"
    
    # Test 7: All numbers M-Pesa code
    test7 = "Payment ID: 1234567890 confirmed"
    result7 = extract_mpesa_code(test7)
    print(f"Test 7: '{test7}' -> {result7}")
    assert result7 == "1234567890", f"Expected '1234567890', got '{result7}'"
    
    print("\n✓ All tests passed!")
