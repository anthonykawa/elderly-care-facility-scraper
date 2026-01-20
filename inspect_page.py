#!/usr/bin/env python3
"""Quick script to inspect the actual page structure."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
chrome_options = Options()
# Don't use headless so we can see what's happening
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Navigating to the page...")
    driver.get("https://www.ccld.dss.ca.gov/carefacilitysearch")
    time.sleep(3)
    
    print("\n--- Page Title ---")
    print(driver.title)
    
    print("\n--- Looking for 'Elderly' links ---")
    page_source = driver.page_source
    
    # Save page source for inspection
    with open('/home/anthony/Projects/old_people_search/page_source.html', 'w') as f:
        f.write(page_source)
    print("Saved page source to page_source.html")
    
    # Try to find any link containing "Elderly"
    from selenium.webdriver.common.by import By
    links = driver.find_elements(By.TAG_NAME, "a")
    
    print(f"\nFound {len(links)} links total")
    print("\nLinks containing 'Elderly':")
    for link in links:
        text = link.text.strip()
        href = link.get_attribute('href')
        if 'elderly' in text.lower() or (href and 'elderly' in href.lower()):
            print(f"  Text: '{text}'")
            print(f"  Href: {href}")
            print(f"  ID: {link.get_attribute('id')}")
            print(f"  Class: {link.get_attribute('class')}")
            print()
    
    # Try to find the facility group section
    print("\n--- Looking for Facility Group section ---")
    try:
        sections = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(sections)} button elements")
        for btn in sections[:10]:  # First 10 buttons
            print(f"  Button text: '{btn.text}' | onclick: {btn.get_attribute('onclick')}")
    except Exception as e:
        print(f"Error finding buttons: {e}")
    
    # Click on Elderly Assisted Living button
    print("\n--- Clicking Elderly Assisted Living button ---")
    try:
        elderly_btn = driver.find_element(By.ID, "fselectorElderlyAssistedLiving")
        print(f"Found button: {elderly_btn.text}")
        elderly_btn.click()
        time.sleep(3)
        
        print("\n--- After clicking, saving new page source ---")
        with open('/home/anthony/Projects/old_people_search/search_page_source.html', 'w') as f:
            f.write(driver.page_source)
        print("Saved search page source to search_page_source.html")
        
        print("\n--- Looking for City input field ---")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} input elements")
        for inp in inputs:
            inp_type = inp.get_attribute('type')
            inp_name = inp.get_attribute('name')
            inp_id = inp.get_attribute('id')
            inp_placeholder = inp.get_attribute('placeholder')
            if inp_type in ['text', 'search'] or 'city' in str(inp_name).lower() or 'city' in str(inp_id).lower():
                print(f"  Type: {inp_type} | Name: {inp_name} | ID: {inp_id} | Placeholder: {inp_placeholder}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to close the browser...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
