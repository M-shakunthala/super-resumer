"""
Simple browser manager for job scraping
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserManager:
    """Simple browser manager for web automation"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize browser manager
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
    
    def get_driver(self) -> webdriver.Chrome:
        """Get or create WebDriver instance"""
        if self.driver is None:
            self.driver = self._initialize_driver()
        return self.driver
    
    def _initialize_driver(self) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        # Persist login session
        chrome_options.add_argument("--user-data-dir=chrome_sessions")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Reduce automation detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Standard options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Additional anti-detection measures
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def close(self):
        """Close browser instance"""
        if self.driver:
            self.driver.quit()
            self.driver = None
