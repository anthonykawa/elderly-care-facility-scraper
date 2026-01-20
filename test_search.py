#!/usr/bin/env python3
"""Test script to complete a search and see results."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    print("Step 1: Navigate to the page...")
    driver.get("https://www.ccld.dss.ca.gov/carefacilitysearch")
    time.sleep(3)
    
    print("Step 2: Click Elderly Assisted Living button...")
    elderly_btn = wait.until(EC.element_to_be_clickable((By.ID, "fselectorElderlyAssistedLiving")))
    elderly_btn.click()
    time.sleep(3)
    
    print("Step 3: Enter city name (Roseville)...")
    city_input = wait.until(EC.presence_of_element_located((By.ID, "city")))
    city_input.clear()
    city_input.send_keys("Roseville")
    
    print("Step 4: Press Enter...")
    city_input.send_keys(Keys.RETURN)
    time.sleep(5)
    
    print("\n--- Results Page ---")
    print(f"Current URL: {driver.current_url}")
    print(f"Page Title: {driver.title}")
    
    # Save results page
    with open('/home/anthony/Projects/old_people_search/results_page_source.html', 'w') as f:
        f.write(driver.page_source)
    print("Saved results page to results_page_source.html")
    
    # Look for facility links/buttons
    print("\n--- Looking for facility View links ---")
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links")
    
    view_links = [link for link in links if 'view' in link.text.lower()]
    print(f"Found {len(view_links)} 'View' links")
    for i, link in enumerate(view_links[:5]):
        print(f"  {i+1}. Text: '{link.text}' | Href: {link.get_attribute('href')}")
    
    # Look for table rows or results
    print("\n--- Looking for results table/structure ---")
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"Found {len(tables)} tables")
    
    # Look for React/Angular table components
    react_tables = driver.find_elements(By.CSS_SELECTOR, "[class*='table'], [class*='result']")
    print(f"Found {len(react_tables)} potential result containers")
    
    input("\nPress Enter to close browser...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
