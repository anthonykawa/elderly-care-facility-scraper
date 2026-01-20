#!/usr/bin/env python3
"""Test with just first facility."""

import sys
sys.path.insert(0, '/home/anthony/Projects/old_people_search')

from scraper import ElderlyFacilityScraper

# Create scraper but modify to only get 1 facility
scraper = ElderlyFacilityScraper("Roseville")

try:
    scraper.navigate_to_search()
    scraper.search_city()
    
    # Get just the first facility
    from selenium.webdriver.common.by import By
    view_links = scraper.driver.find_elements(By.LINK_TEXT, "view")
    if view_links:
        url = view_links[0].get_attribute('href')
        print(f"\nTesting with first facility: {url}\n")
        facility_data = scraper.scrape_facility_details(url)
        print(f"\n=== RESULT ===")
        print(f"Name: '{facility_data['Name']}'")
        print(f"Status: '{facility_data['Status']}'")
        print(f"Address: '{facility_data['Address']}'")
        print(f"Phone: '{facility_data['Phone Number']}'")
        print(f"Capacity: '{facility_data['Facility Capacity']}'")
finally:
    scraper.driver.quit()
