#!/usr/bin/env python3
"""Test script to view a facility detail page."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    print("Navigate to facility detail page...")
    driver.get("https://www.ccld.dss.ca.gov/carefacilitysearch/FacDetail/315920367")
    time.sleep(5)
    
    print(f"Page Title: {driver.title}")
    print(f"Current URL: {driver.current_url}")
    
    # Save page source
    with open('/home/anthony/Projects/old_people_search/facility_detail.html', 'w') as f:
        f.write(driver.page_source)
    print("Saved facility detail page to facility_detail.html")
    
    # Look for key information
    print("\n--- Looking for Facility Info ---")
    
    # Look for headers
    headers = driver.find_elements(By.TAG_NAME, "h1") + driver.find_elements(By.TAG_NAME, "h2") + driver.find_elements(By.TAG_NAME, "h3")
    print(f"Found {len(headers)} headers:")
    for h in headers[:5]:
        if h.text.strip():
            print(f"  {h.text}")
    
    # Look for paragraphs and divs with content
    print("\n--- Text content preview ---")
    text = driver.find_element(By.TAG_NAME, "body").text
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:30]:
        print(f"  {line}")
    
    input("\nPress Enter to close browser...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
