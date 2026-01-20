#!/usr/bin/env python3
"""Debug script to check actual page structure."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = "https://www.ccld.dss.ca.gov/carefacilitysearch/FacDetail/315920367"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(3)
    
    body_text = driver.find_element(By.TAG_NAME, "body").text
    
    print("\n=== FIRST 2000 CHARACTERS ===")
    print(repr(body_text[:2000]))
    
    print("\n\n=== SEARCHING FOR 'Facility Detail' ===")
    idx = body_text.find("Facility Detail")
    if idx != -1:
        print(f"Found at index {idx}")
        print("Context (500 chars after):")
        print(repr(body_text[idx:idx+500]))
    
    print("\n\n=== TESTING PATTERNS ===")
    
    # Try different patterns
    patterns = [
        (r'Facility Detail\s+([^\n]+?)\s+Status:', "Original pattern"),
        (r'Facility Detail\s*\n\s*([^\n]+)\s+Status:', "With explicit newline"),
        (r'Facility Detail[^\n]*\n\s*([^S]+?)\s+Status:', "Different approach"),
        (r'Facility Detail.*?\n\s*(.+?)\s{2,}Status:', "More flexible"),
    ]
    
    for pattern, desc in patterns:
        match = re.search(pattern, body_text, re.DOTALL)
        if match:
            print(f"\n✓ {desc}: '{match.group(1).strip()}'")
        else:
            print(f"\n✗ {desc}: No match")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
