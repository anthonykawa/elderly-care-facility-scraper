#!/usr/bin/env python3
"""Quick test of single facility scraping."""

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
    url = "https://www.ccld.dss.ca.gov/carefacilitysearch/FacDetail/342701453"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(3)
    
    body_text = driver.find_element(By.TAG_NAME, "body").text
    print("\n--- Body Text ---")
    print(body_text[:1000])
    
    facility_data = {
        'Name': '',
        'Status': '',
        'Address': '',
        'Phone Number': '',
        'Facility Capacity': ''
    }
    
    # Extract facility name
    name_match = re.search(r'Facility Detail\s+([^\n]+?)\s+Status:', body_text, re.DOTALL)
    if name_match:
        facility_data['Name'] = name_match.group(1).strip()
        print(f"\nName: {facility_data['Name']}")
    
    # Extract status
    status_match = re.search(r'Status:\s*([^\n]+)', body_text)
    if status_match:
        facility_data['Status'] = status_match.group(1).strip()
        print(f"Status: {facility_data['Status']}")
    
    # Extract address
    address_match = re.search(r'Address:\s*\n([^\n]+)\n([^\n]+)', body_text)
    if address_match:
        street = address_match.group(1).strip()
        city_state_zip = address_match.group(2).strip()
        facility_data['Address'] = f"{street}, {city_state_zip}"
        print(f"Address: {facility_data['Address']}")
    
    # Extract phone
    phone_match = re.search(r'Phone:\s*([^\n]+)', body_text)
    if phone_match:
        facility_data['Phone Number'] = phone_match.group(1).strip()
        print(f"Phone: {facility_data['Phone Number']}")
    
    # Extract capacity
    capacity_match = re.search(r'Facility Capacity:\s*(\d+)', body_text)
    if capacity_match:
        facility_data['Facility Capacity'] = capacity_match.group(1).strip()
        print(f"Capacity: {facility_data['Facility Capacity']}")
    
    print("\n--- Final Data ---")
    print(facility_data)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
