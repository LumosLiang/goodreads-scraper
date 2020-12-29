from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

class Browser(Chrome):
    OPTIONS = {"goog:chromeOptions": {
        # Disable images loading    
        "prefs": {"profile.managed_default_content_settings.images": 2},
        # Disable Chrome's GUI
        "args": ["--headless", "--disable-gpu"]
    }}

    def __init__(self):
        Chrome.__init__(self, desired_capabilities=self.OPTIONS)
        # Initialize browsing counters
        self.rating = self.sort = self.fails = None

    def goto_next_page(self):
         # Try to find the next button
        try:
            next_page_element = self.find_element_by_class_name('next_page')
            self.execute_script("arguments[0].click();", next_page_element) 
            return True
        # Return none if there isn't one
        except EC.NoSuchElementException:
            print("WARNING: There is no next page!")
            return None
        except EC.WebDriverException:
            print("WARNING: Retrying to goto next page!")
            self.implicitly_wait(1)
            return self.goto_next_page()