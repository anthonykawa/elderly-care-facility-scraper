#!/usr/bin/env python3
"""
Elderly Care Facility Scraper - GUI Version
Cross-platform GUI application for scraping elderly care facilities in California.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os
from scraper import ElderlyFacilityScraper


class ScraperGUI:
    """GUI application for the elderly care facility scraper."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Elderly Care Facility Scraper")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.city_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        self.is_scraping = False
        self.scraper = None
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="California Elderly Care Facility Scraper",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # City input
        city_label = ttk.Label(main_frame, text="City Name:", font=("Arial", 10))
        city_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.city_entry = ttk.Entry(main_frame, textvariable=self.city_var, width=30, font=("Arial", 10))
        self.city_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        self.city_entry.focus()
        
        # Bind Enter key to start scraping
        self.city_entry.bind('<Return>', lambda e: self.start_scraping())
        
        # Output directory input
        output_label = ttk.Label(main_frame, text="Output Folder:", font=("Arial", 10))
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_dir_var, width=30, font=("Arial", 10))
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        
        # Browse button
        self.browse_button = ttk.Button(
            main_frame,
            text="Browse...",
            command=self.browse_folder,
            width=15
        )
        self.browse_button.grid(row=2, column=2, pady=5, padx=(5, 0))
        
        # Start button
        self.start_button = ttk.Button(
            main_frame, 
            text="Start Scraping", 
            command=self.start_scraping,
            width=15
        )
        self.start_button.grid(row=3, column=2, pady=5, padx=(5, 0))
        
        # Stop button (initially disabled)
        self.stop_button = ttk.Button(
            main_frame,
            text="Stop",
            command=self.stop_scraping,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=4, column=2, pady=5, padx=(5, 0))
        
        # Progress label
        self.progress_label = ttk.Label(main_frame, text="Ready to scrape", font=("Arial", 9))
        self.progress_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Output text area
        output_label = ttk.Label(main_frame, text="Output:", font=("Arial", 10))
        output_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            width=80,
            height=25,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.output_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8)
        )
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def log_output(self, message):
        """Add a message to the output text area."""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update the status bar."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def update_progress(self, message):
        """Update the progress label."""
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.output_dir_var.get()
        )
        if folder:
            self.output_dir_var.set(folder)
            self.log_output(f"Output folder set to: {folder}")
        
    def start_scraping(self):
        """Start the scraping process in a separate thread."""
        city = self.city_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            self.city_entry.focus()
            return
        
        if not output_dir:
            messagebox.showwarning("Output Folder Required", "Please select an output folder.")
            return
        
        # Validate output directory
        if not os.path.exists(output_dir):
            result = messagebox.askyesno(
                "Create Folder?",
                f"The folder '{output_dir}' does not exist.\n\nDo you want to create it?"
            )
            if result:
                try:
                    os.makedirs(output_dir)
                    self.log_output(f"Created output folder: {output_dir}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create folder:\n\n{e}")
                    return
            else:
                return
        
        if self.is_scraping:
            messagebox.showinfo("Already Running", "Scraping is already in progress.")
            return
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Update UI state
        self.is_scraping = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.city_entry.config(state=tk.DISABLED)
        self.output_entry.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        
        # Start scraping in a separate thread
        thread = threading.Thread(target=self.run_scraper, args=(city, output_dir), daemon=True)
        thread.start()
        
    def stop_scraping(self):
        """Stop the scraping process."""
        if self.scraper:
            self.log_output("\n⚠ Stopping scraper... Please wait...")
            self.update_status("Stopping...")
            # The scraper will be stopped when the driver quits
            # The thread will notice and exit gracefully
            
    def run_scraper(self, city, output_dir):
        """Run the scraper (called in a separate thread)."""
        try:
            self.update_status(f"Scraping facilities in {city}...")
            self.update_progress("Initializing...")
            self.log_output(f"Starting scraper for {city}...")
            self.log_output(f"Output folder: {output_dir}")
            self.log_output("=" * 50)
            
            # Create custom scraper with GUI logging
            self.scraper = GUIElderlyFacilityScraper(city, self, output_dir)
            self.scraper.run()
            
            self.log_output("=" * 50)
            self.log_output("Scraping completed!")
            
            if self.scraper.facilities:
                self.update_status(f"Completed! Found {len(self.scraper.facilities)} facilities")
                self.update_progress(f"✓ Completed - {len(self.scraper.facilities)} facilities found")
                messagebox.showinfo(
                    "Success",
                    f"Scraping completed!\n\nFound {len(self.scraper.facilities)} facilities.\n\nData saved to: {self.scraper.filename}"
                )
            else:
                self.update_status("Completed - No facilities found")
                self.update_progress("✓ Completed - No facilities found")
                messagebox.showinfo("Complete", f"No facilities found in {city}.")
                
        except Exception as e:
            self.log_output(f"\n✗ Error: {e}")
            self.update_status("Error occurred")
            self.update_progress("✗ Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            
        finally:
            # Reset UI state
            self.is_scraping = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.city_entry.config(state=tk.NORMAL)
            self.output_entry.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            self.scraper = None


class GUIElderlyFacilityScraper(ElderlyFacilityScraper):
    """Extended scraper that logs to GUI instead of console."""
    
    def __init__(self, city, gui, output_dir=None):
        """Initialize with GUI reference."""
        super().__init__(city, output_dir)
        self.gui = gui
        
    def navigate_to_search(self):
        """Navigate to the elderly assisted living search page."""
        self.gui.log_output(f"Navigating to {self.base_url}...")
        self.gui.update_progress("Loading website...")
        self.driver.get(self.base_url + "/carefacilitysearch")
        
        # Wait for Angular to load
        self.gui.log_output("Waiting for page to load...")
        import time
        time.sleep(5)
        
        # Click on "Elderly Assisted Living" button
        self.gui.log_output("Clicking on 'Elderly Assisted Living' button...")
        self.gui.update_progress("Navigating to search form...")
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            elderly_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "fselectorElderlyAssistedLiving"))
            )
            elderly_button.click()
        except TimeoutException:
            self.gui.log_output("Could not find 'Elderly Assisted Living' button by ID. Trying button text...")
            elderly_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Elderly Assisted Living')]"))
            )
            elderly_button.click()
        
        time.sleep(3)
        
    def search_city(self):
        """Enter the city name and submit the search."""
        self.gui.log_output(f"Searching for facilities in {self.city}...")
        self.gui.update_progress(f"Searching for {self.city}...")
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support import expected_conditions as EC
        import time
        
        city_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "city"))
        )
        
        city_input.clear()
        city_input.send_keys(self.city)
        city_input.send_keys(Keys.RETURN)
        
        time.sleep(5)
        
    def scrape_results_page(self):
        """Scrape all facilities from the current results page."""
        self.gui.log_output("Scraping facilities from current page...")
        
        from selenium.webdriver.common.by import By
        import time
        
        page_facilities = []
        
        try:
            view_links = self.driver.find_elements(By.LINK_TEXT, "view")
            
            if not view_links:
                view_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='FacDetail']")
            
            facility_urls = [link.get_attribute('href') for link in view_links]
            
            self.gui.log_output(f"Found {len(facility_urls)} facilities on this page")
            
            if len(facility_urls) == 0:
                return page_facilities
            
            for idx, url in enumerate(facility_urls, 1):
                self.gui.update_progress(f"Scraping facility {idx}/{len(facility_urls)}...")
                facility_data = self.scrape_facility_details(url)
                if facility_data['Name']:
                    page_facilities.append(facility_data)
                    self.facilities.append(facility_data)
                    self.gui.log_output(f"✓ Added: {facility_data['Name']}")
                else:
                    self.gui.log_output(f"✗ Failed to get name for {url}")
                    page_facilities.append(facility_data)
                    self.facilities.append(facility_data)
                time.sleep(1)
            
            return page_facilities
            
        except Exception as e:
            self.gui.log_output(f"Error scraping results page: {e}")
            import traceback
            self.gui.log_output(traceback.format_exc())
            return page_facilities
    
    def scrape_all_pages(self):
        """Scrape facilities from all pages."""
        page_num = 1
        
        while True:
            self.gui.log_output(f"\n--- Scraping page {page_num} ---")
            self.gui.update_progress(f"Scraping page {page_num}...")
            page_facilities = self.scrape_results_page()
            
            if len(page_facilities) == 0:
                self.gui.log_output("No facilities found on this page. Stopping pagination.")
                break
            
            self.append_to_csv(page_facilities, is_first_page=(page_num == 1))
            
            if self.has_next_page():
                self.gui.log_output("Moving to next page...")
                self.go_to_next_page()
                page_num += 1
            else:
                self.gui.log_output("No more pages to scrape.")
                break
        
        self.scraping_completed = True
    
    def append_to_csv(self, facilities, is_first_page=False):
        """Append facilities to CSV file after each page is scraped."""
        if not facilities:
            return
        
        import csv
        mode = 'w' if is_first_page else 'a'
        
        self.gui.log_output(f"Writing {len(facilities)} facilities to {self.filename}...")
        
        with open(self.filename, mode, newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Status', 'Address', 'Phone Number', 'Facility Capacity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if is_first_page:
                writer.writeheader()
            
            for facility in facilities:
                writer.writerow(facility)
        
        self.gui.log_output(f"✓ Wrote to {self.filename}")
    
    def run(self):
        """Run the complete scraping process."""
        try:
            self.navigate_to_search()
            self.search_city()
            self.scrape_all_pages()
            
            if self.scraping_completed:
                self.gui.log_output(f"\n✓ Scraping completed successfully! Total facilities: {len(self.facilities)}")
                self.gui.log_output(f"Data saved to: {self.filename}")
        except Exception as e:
            self.gui.log_output(f"\n✗ ERROR: An error occurred during scraping: {e}")
            import traceback
            self.gui.log_output(traceback.format_exc())
        finally:
            if not self.scraping_completed:
                if self.facilities:
                    self.gui.log_output(f"\n⚠ WARNING: Scraping was interrupted! Partial data ({len(self.facilities)} facilities) saved to: {self.filename}")
                else:
                    self.gui.log_output(f"\n✗ ERROR: Scraping failed - no data was collected.")
            
            self.gui.log_output("\nClosing browser...")
            self.gui.update_progress("Cleaning up...")
            self.driver.quit()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = ScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
