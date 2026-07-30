"""
Automated Screenshot Capture Script
Uses Selenium to capture screenshots of the running dashboard
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ScreenshotCapture:
    """Capture automated screenshots of the AI Job Agent dashboard."""
    
    def __init__(self, base_url="http://localhost:8501"):
        self.base_url = base_url
        self.screenshot_dir = "screenshots"
        self.driver = None
        
    def setup_driver(self):
        """Initialize Selenium Chrome driver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def capture_screenshot(self, filename, element_selector=None):
        """
        Capture screenshot of current page or specific element.
        
        Args:
            filename: Name for the screenshot file
            element_selector: CSS selector for specific element (optional)
        """
        if not self.driver:
            self.setup_driver()
        
        try:
            if element_selector:
                element = self.driver.find_element("css selector", element_selector)
                element.screenshot(f"{self.screenshot_dir}/{filename}")
            else:
                self.driver.save_screenshot(f"{self.screenshot_dir}/{filename}")
            
            print(f"✅ Captured: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to capture {filename}: {str(e)}")
            return False
    
    def capture_dashboard_overview(self):
        """Capture main dashboard overview."""
        self.driver.get(self.base_url)
        time.sleep(3)  # Wait for page to load
        return self.capture_screenshot("dashboard_overview.png")
    
    def capture_job_tracking(self):
        """Capture job tracking table section."""
        self.driver.get(self.base_url)
        time.sleep(3)
        # Assuming there's a job tracking section
        return self.capture_screenshot("job_tracking_table.png")
    
    def capture_resume_tailoring(self):
        """Capture resume tailoring interface."""
        self.driver.get(f"{self.base_url}?page=resume_tailoring")
        time.sleep(3)
        return self.capture_screenshot("resume_tailoring_example.png")
    
    def capture_apply_log(self):
        """Capture application log section."""
        self.driver.get(f"{self.base_url}?page=logs")
        time.sleep(3)
        return self.capture_screenshot("successful_apply_log.png")
    
    def capture_all_screenshots(self):
        """Capture all required screenshots."""
        print("🎯 Starting automated screenshot capture...")
        print(f"📍 Target URL: {self.base_url}")
        print(f"📁 Output directory: {self.screenshot_dir}")
        
        # Ensure directory exists
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        results = {
            "dashboard_overview": self.capture_dashboard_overview(),
            "job_tracking": self.capture_job_tracking(),
            "resume_tailoring": self.capture_resume_tailoring(),
            "apply_log": self.capture_apply_log()
        }
        
        self.close()
        
        # Summary
        successful = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\n📊 Screenshot Capture Summary:")
        print(f"   ✅ Successful: {successful}/{total}")
        print(f"   ❌ Failed: {total - successful}/{total}")
        
        return results
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()


def main():
    """Main execution function."""
    print("📸 AI Job Agent - Automated Screenshot Capture")
    print("=" * 50)
    
    # Check if dashboard is running
    import requests
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code != 200:
            print("⚠️  Dashboard may not be running at http://localhost:8501")
            print("Please start the dashboard first: streamlit run ui/dashboard.py")
            return
    except requests.exceptions.RequestException:
        print("⚠️  Cannot connect to dashboard at http://localhost:8501")
        print("Please start the dashboard first: streamlit run ui/dashboard.py")
        return
    
    # Capture screenshots
    capturer = ScreenshotCapture()
    capturer.capture_all_screenshots()
    
    print("\n🎉 Screenshot capture complete!")
    print("📁 Check the screenshots/ directory for results")


if __name__ == "__main__":
    main()