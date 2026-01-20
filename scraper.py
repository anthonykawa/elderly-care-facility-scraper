#!/usr/bin/env python3
"""
Elderly Care Facility Scraper
Scrapes elderly care facility information from the California Community Care Licensing Division website.
"""

import sys
import csv
import time
import re
import argparse
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class ElderlyFacilityScraper:
    """Scraper for elderly care facilities in California."""
    
    def __init__(self, city, output_dir=None):
        """Initialize the scraper with a city name and optional output directory."""
        self.city = city
        self.base_url = "https://www.ccld.dss.ca.gov"
        self.facilities = []
        self.scraping_completed = False
        self.output_dir = output_dir or os.getcwd()
        
        # Ensure output directory exists
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        filename = f"{self.city.lower().replace(' ', '-')}-elderly-facilities.csv"
        self.filename = os.path.join(self.output_dir, filename)
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize the driver
        # Check if running as a frozen app (PyInstaller)
        if getattr(sys, 'frozen', False):
            # Running as bundled app - look for bundled chromedriver
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                bundled_chromedriver = os.path.join(sys._MEIPASS, 'chromedriver')
                if os.path.exists(bundled_chromedriver):
                    service = Service(bundled_chromedriver)
                else:
                    # Fallback to system chromedriver
                    chromedriver_path = shutil.which('chromedriver')
                    if chromedriver_path:
                        service = Service(chromedriver_path)
                    else:
                        raise RuntimeError(
                            "ChromeDriver not found. Please install it:\n"
                            "  brew install chromedriver"
                        )
            else:
                service = Service()  # Let Selenium Manager handle it
        else:
            # Running as script - let Selenium Manager auto-download
            service = Service()
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def navigate_to_search(self):
        """Navigate to the elderly assisted living search page."""
        print(f"Navigating to {self.base_url}...")
        self.driver.get(self.base_url + "/carefacilitysearch")
        
        # Wait for Angular to load - wait for buttons to be present
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Click on "Elderly Assisted Living" button
        print("Clicking on 'Elderly Assisted Living' button...")
        try:
            elderly_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "fselectorElderlyAssistedLiving"))
            )
            elderly_button.click()
        except TimeoutException:
            print("Could not find 'Elderly Assisted Living' button by ID. Trying button text...")
            elderly_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Elderly Assisted Living')]"))
            )
            elderly_button.click()
        
        time.sleep(3)  # Wait for page to load
    
    def search_city(self):
        """Enter the city name and submit the search."""
        print(f"Searching for facilities in {self.city}...")
        
        # Find the city input field by ID
        city_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "city"))
        )
        
        # Clear and enter city name
        city_input.clear()
        city_input.send_keys(self.city)
        
        # Press Enter
        city_input.send_keys(Keys.RETURN)
        
        time.sleep(5)  # Wait for results to load
    
    def scrape_facility_details(self, facility_url):
        """Scrape details from a single facility page."""
        # Fix relative URLs - ensure they have the full path
        if facility_url.startswith('/FacDetail'):
            facility_url = f"{self.base_url}/carefacilitysearch{facility_url}"
        elif '/FacDetail/' in facility_url and '/carefacilitysearch/' not in facility_url:
            # Fix URLs that are missing /carefacilitysearch/
            facility_url = facility_url.replace('/FacDetail/', '/carefacilitysearch/FacDetail/')
        
        print(f"Scraping facility: {facility_url}")
        
        # Open facility page in a new window
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(facility_url)
        
        # Wait for page to load - wait for body content
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)  # Additional wait for Angular/dynamic content
        except TimeoutException:
            print("Warning: Page load timeout")
            time.sleep(2)
        
        facility_data = {
            'Name': '',
            'Status': '',
            'Address': '',
            'Phone Number': '',
            'Facility Capacity': ''
        }
        
        try:
            # Get the body text which contains all facility details
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Debug: Log if body is too short
            if len(body_text) < 100:
                print(f"Warning: Page body too short ({len(body_text)} chars), may not have loaded properly")
                print(f"Body preview: {body_text[:200]}")
            
            # Extract facility name (first line after "Facility Detail")
            name_match = re.search(r'Facility Detail\s+([^\n]+?)\s+Status:', body_text, re.DOTALL)
            if name_match:
                facility_data['Name'] = name_match.group(1).strip()
            else:
                print(f"Debug: Could not find name. Body preview: {body_text[:300]}")
            
            # Extract status
            status_match = re.search(r'Status:\s*([^\n]+)', body_text)
            if status_match:
                facility_data['Status'] = status_match.group(1).strip()
            
            # Extract address (lines between "Address:" and "Licensee Name:")
            address_match = re.search(r'Address:\s*\n([^\n]+)\n([^\n]+)', body_text)
            if address_match:
                # Get the street and city/state/zip lines
                street = address_match.group(1).strip()
                city_state_zip = address_match.group(2).strip()
                facility_data['Address'] = f"{street}, {city_state_zip}"
            
            # Extract phone number
            phone_match = re.search(r'Phone:\s*([^\n]+)', body_text)
            if phone_match:
                facility_data['Phone Number'] = phone_match.group(1).strip()
            
            # Extract capacity
            capacity_match = re.search(r'Facility Capacity:\s*(\d+)', body_text)
            if capacity_match:
                facility_data['Facility Capacity'] = capacity_match.group(1).strip()
        
        except Exception as e:
            print(f"Error scraping facility details: {e}")
            import traceback
            traceback.print_exc()
        
        # Close the facility tab and return to results page
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        return facility_data
    
    def scrape_results_page(self):
        """Scrape all facilities from the current results page."""
        print("Scraping facilities from current page...")
        
        page_facilities = []
        
        try:
            # Find all "view" links for facilities (lowercase)
            view_links = self.driver.find_elements(By.LINK_TEXT, "view")
            
            if not view_links:
                # Try alternative selector
                view_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='FacDetail']")
            
            # Get all facility URLs first
            facility_urls = [link.get_attribute('href') for link in view_links]
            
            print(f"Found {len(facility_urls)} facilities on this page")
            
            # Return empty list if no facilities
            if len(facility_urls) == 0:
                return page_facilities
            
            # Scrape each facility
            for url in facility_urls:
                facility_data = self.scrape_facility_details(url)
                if facility_data['Name']:  # Only add if we got at least the name
                    page_facilities.append(facility_data)
                    self.facilities.append(facility_data)
                    print(f"✓ Added facility: {facility_data['Name']}")
                else:
                    print(f"✗ Failed to get name for {url}")
                    # Add it anyway with whatever data we have
                    page_facilities.append(facility_data)
                    self.facilities.append(facility_data)
                time.sleep(1)  # Be nice to the server
            
            return page_facilities
        
        except Exception as e:
            print(f"Error scraping results page: {e}")
            import traceback
            traceback.print_exc()
            return page_facilities
    
    def has_next_page(self):
        """Check if there's a next page in pagination."""
        try:
            # Look for "Next »" span element
            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next »')]")
            # Check if parent li is disabled
            parent_li = next_button.find_element(By.XPATH, "./..")
            return 'disabled' not in parent_li.get_attribute('class')
        except NoSuchElementException:
            return False
    
    def go_to_next_page(self):
        """Navigate to the next page of results."""
        # Click on "Next »" span element
        next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next »')]")
        next_button.click()
        
        time.sleep(3)  # Wait for page to load
    
    def scrape_all_pages(self):
        """Scrape facilities from all pages."""
        page_num = 1
        
        while True:
            print(f"\n--- Scraping page {page_num} ---")
            page_facilities = self.scrape_results_page()
            
            # Stop if no facilities found on this page
            if len(page_facilities) == 0:
                print("No facilities found on this page. Stopping pagination.")
                break
            
            # Write this page's facilities to CSV
            self.append_to_csv(page_facilities, is_first_page=(page_num == 1))
            
            if self.has_next_page():
                print("Moving to next page...")
                self.go_to_next_page()
                page_num += 1
            else:
                print("No more pages to scrape.")
                break
        
        # Mark scraping as completed
        self.scraping_completed = True
    
    def append_to_csv(self, facilities, is_first_page=False):
        """Append facilities to CSV file after each page is scraped."""
        if not facilities:
            return
        
        mode = 'w' if is_first_page else 'a'
        
        print(f"Writing {len(facilities)} facilities to {self.filename}...")
        
        with open(self.filename, mode, newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Status', 'Address', 'Phone Number', 'Facility Capacity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header only on first page
            if is_first_page:
                writer.writeheader()
            
            for facility in facilities:
                writer.writerow(facility)
        
        print(f"✓ Wrote to {self.filename}")
    
    def run(self):
        """Run the complete scraping process."""
        try:
            self.navigate_to_search()
            self.search_city()
            self.scrape_all_pages()
            
            if self.scraping_completed:
                print(f"\n✓ Scraping completed successfully! Total facilities: {len(self.facilities)}")
                print(f"Data saved to: {self.filename}")
        except Exception as e:
            print(f"\n✗ ERROR: An error occurred during scraping: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if not self.scraping_completed:
                if self.facilities:
                    print(f"\n⚠ WARNING: Scraping was interrupted! Partial data ({len(self.facilities)} facilities) saved to: {self.filename}")
                else:
                    print(f"\n✗ ERROR: Scraping failed - no data was collected.")
            
            print("\nClosing browser...")
            self.driver.quit()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Scrape elderly care facilities in California cities.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py "Los Angeles"
  python scraper.py "San Francisco" --output-dir /path/to/folder
  python scraper.py "Sacramento" -o ./output
        """
    )
    
    parser.add_argument(
        'city',
        type=str,
        help='Name of the California city to search for facilities'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='Directory where CSV file will be saved (default: current directory)'
    )
    
    args = parser.parse_args()
    
    print(f"Starting scraper for {args.city}...")
    if args.output_dir:
        print(f"Output directory: {os.path.abspath(args.output_dir)}")
    print("=" * 50)
    
    scraper = ElderlyFacilityScraper(args.city, args.output_dir)
    scraper.run()
    
    print("=" * 50)
    print("Scraping completed!")


if __name__ == "__main__":
    main()
